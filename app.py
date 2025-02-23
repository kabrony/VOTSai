import streamlit as st
import asyncio
import os
import sqlite3
import subprocess
from collections import deque
from core.models import ModelFactory
from core.memory import init_memory_db, update_memory, get_relevant_memory
from core.classifier import IntentClassifier
from handlers.query import orchestrate_query
from utils.constants import SHORT_TERM_MAX
from agents.codeAgent import analyze_code
import logging
import datetime
import pandas as pd
import altair as alt
import ollama

# Logging setup
logging.basicConfig(filename="vots_agi.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# SQLite datetime adapter
def adapt_datetime(dt):
    return dt.isoformat()

sqlite3.register_adapter(datetime.datetime, adapt_datetime)

def load_env():
    """Load environment variables from .env file."""
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
    if "PERPLEXITY_API_KEY" not in os.environ or "DEEPSEEK_API_KEY" not in os.environ:
        st.error("⚠️ Missing API keys. Set PERPLEXITY_API_KEY and DEEPSEEK_API_KEY in .env or Streamlit secrets.")
        return False
    return True

def ensure_playwright_installed():
    """Ensure Playwright browsers are installed."""
    playwright_dir = os.path.expanduser("~/.cache/ms-playwright")
    if not os.path.exists(playwright_dir) or not any(os.path.isdir(os.path.join(playwright_dir, d)) for d in os.listdir(playwright_dir)):
        st.warning("Playwright browsers not found. Installing now...")
        try:
            process = subprocess.run(["python", "-m", "playwright", "install", "chromium"], check=True, capture_output=True, text=True)
            logger.info(f"Playwright install output: {process.stdout}")
            st.success("Playwright browsers installed successfully!")
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to install Playwright browsers: {e.stderr}")
            logger.error(f"Playwright installation failed: {e.stderr}")
            return False
    return True

def preprocess_query(query):
    """Preprocess query and detect crawl intent."""
    query = query.strip()
    is_crawl = query.lower().startswith("crawl ")
    if is_crawl:
        url = query[6:].strip()
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("file://") or url.startswith("raw:")):
            query = f"crawl https://{url}"
            st.info(f"Added 'https://' to URL: {query}")
            logger.info(f"Preprocessed query: {query}")
    query = f"{query} [Use chain-of-thought reasoning and deep research style to generate a detailed, creative response up to the maximum token limit]"
    return query, is_crawl

def analyze_response_with_r1(response, query, memory_context, is_crawl=False):
    """Analyze and refine response using DeepSeek R1 Latest via Ollama, tailored to query type."""
    try:
        logger.info("Attempting R1 analysis with Ollama using deepseek-r1:latest")
        if is_crawl:
            prompt = (
                f"Original Query: {query}\n"
                f"Initial Response (Web Crawl Summary): {response}\n"
                f"Memory Context: {memory_context}\n\n"
                "Using chain-of-thought reasoning, analyze the initial web crawl summary for accuracy, completeness, and relevance to the query. "
                "Provide a detailed, creative enhancement of the website’s purpose, structure, and potential features, "
                "incorporating memory context (e.g., past web or system-related queries) for consistency and depth. "
                "Return the enhanced description followed by a detailed analysis section."
            )
        else:
            prompt = (
                f"Original Query: {query}\n"
                f"Initial Response: {response}\n"
                f"Memory Context: {memory_context}\n\n"
                "Using chain-of-thought reasoning, analyze the initial response for accuracy, functionality, and adherence to the query’s intent. "
                "If the query requests a script, generate an improved version with robust error handling, performance optimizations, and enhancements (e.g., alerts for high usage), "
                "incorporating memory context (e.g., past log-related queries) for consistency and depth. "
                "Return the refined script followed by a detailed analysis section."
            )
        r1_response = ollama.generate(model="deepseek-r1:latest", prompt=prompt)
        return r1_response["response"]
    except Exception as e:
        logger.error(f"R1 analysis failed: {str(e)}")
        return f"{response}\n\n**Analysis**: R1 analysis unavailable due to error: {str(e)}"

def get_directory_contents():
    """Return formatted list of current directory contents."""
    dir_path = os.getcwd()
    try:
        contents = os.listdir(dir_path)
        return "\n".join([f"- {item}" + (" (dir)" if os.path.isdir(os.path.join(dir_path, item)) else "") for item in contents])
    except Exception as e:
        logger.error(f"Failed to list directory contents: {str(e)}")
        return "Error: Unable to list directory contents."

def update_database_schema(conn):
    """Update long_term_memory table schema if needed."""
    try:
        c = conn.cursor()
        c.execute("PRAGMA table_info(long_term_memory)")
        columns = {col[1] for col in c.fetchall()}
        
        for col, col_type in [("model", "TEXT"), ("latency", "REAL"), ("input_tokens", "INTEGER"), ("output_tokens", "INTEGER")]:
            if col not in columns:
                c.execute(f"ALTER TABLE long_term_memory ADD COLUMN {col} {col_type}")
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to update database schema: {str(e)}")
        st.error(f"Database schema update failed: {str(e)}")

def generate_daily_report(conn, short_term_memory):
    """Generate a daily report of queries from memory."""
    today = datetime.datetime.now().date()
    today_str = today.isoformat()
    report_data = {"Timestamp": [], "Query": [], "Result": [], "Model": [], "Latency": [], "Input Tokens": [], "Output Tokens": []}
    
    for entry in short_term_memory:
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.datetime.now().isoformat()
        entry_date = datetime.datetime.fromisoformat(entry["timestamp"]).date()
        if entry_date == today:
            report_data["Timestamp"].append(entry["timestamp"])
            report_data["Query"].append(entry["query"])
            report_data["Result"].append(entry["answer"][:100] + "..." if len(entry["answer"]) > 100 else entry["answer"])
            report_data["Model"].append(entry.get("model", "Unknown"))
            report_data["Latency"].append(entry.get("latency", 0))
            report_data["Input Tokens"].append(entry.get("input_tokens", 0))
            report_data["Output Tokens"].append(entry.get("output_tokens", 0))
    
    try:
        c = conn.cursor()
        c.execute("SELECT timestamp, query, answer, model, latency, input_tokens, output_tokens FROM long_term_memory WHERE DATE(timestamp) = ?", (today_str,))
        for row in c.fetchall():
            report_data["Timestamp"].append(row[0])
            report_data["Query"].append(row[1])
            report_data["Result"].append(row[2][:100] + "..." if len(row[2]) > 100 else row[2])
            report_data["Model"].append(row[3] if row[3] else "Unknown")
            report_data["Latency"].append(row[4] if row[4] is not None else 0)
            report_data["Input Tokens"].append(row[5] if row[5] is not None else 0)
            report_data["Output Tokens"].append(row[6] if row[6] is not None else 0)
    except sqlite3.Error as e:
        logger.error(f"Failed to fetch daily report data: {str(e)}")
    
    return pd.DataFrame(report_data)

def main():
    """Main function for VOTSai application."""
    st.set_page_config(page_title="VOTSai V1.4.4", layout="wide", initial_sidebar_state="expanded", page_icon="🧠")
    
    # Initialize session state
    if "short_term_memory" not in st.session_state:
        st.session_state.short_term_memory = deque(maxlen=SHORT_TERM_MAX)
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "Auto"
    if "web_priority" not in st.session_state:
        st.session_state.web_priority = True
    if "timeout" not in st.session_state:
        st.session_state.timeout = 60
    if "share_format" not in st.session_state:
        st.session_state.share_format = "Text"
    if "creativity_level" not in st.session_state:
        st.session_state.creativity_level = 50
    if "telemetry_data" not in st.session_state:
        st.session_state.telemetry_data = deque(maxlen=1000)  # Cap telemetry to prevent memory issues

    if not load_env():
        return

    if not ensure_playwright_installed():
        return

    conn = init_memory_db("vots_agi_memory.db")
    update_database_schema(conn)
    model_factory = ModelFactory()
    intent_classifier = IntentClassifier()

    # Cyberpunk neon footer CSS
    footer_style = """
    <style>
    .cyberpunk-footer {
        position: fixed;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        color: #00FF00;
        text-shadow: 0 0 5px #00FF00, 0 0 10px #00FF00, 0 0 20px #00FF00;
        animation: matrix 1.5s infinite alternate;
    }
    @keyframes matrix {
        from { opacity: 0.7; }
        to { opacity: 1; }
    }
    .cyberpunk-footer a {
        color: #00FF00;
        text-decoration: none;
    }
    .cyberpunk-footer a:hover {
        text-shadow: 0 0 10px #00FF00, 0 0 20px #00FF00, 0 0 30px #00FF00;
    }
    </style>
    """
    st.markdown(footer_style, unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ AI Configuration")
        model_options = ["Auto", "Perplexity API", "DeepSeek API", "Local DeepSeek"]
        st.session_state.selected_model = st.selectbox("Model Selection", model_options, index=model_options.index(st.session_state.selected_model))
        st.session_state.web_priority = st.toggle("🌐 Web Integration", value=st.session_state.web_priority)
        st.session_state.creativity_level = st.slider("🧠 Creativity Level", 0, 100, st.session_state.creativity_level)
        st.session_state.timeout = st.slider("Timeout (s)", 10, 120, st.session_state.timeout)
        if st.button("Clear Memory"):
            st.session_state.short_term_memory.clear()
            try:
                conn.execute("DELETE FROM long_term_memory")
                conn.commit()
            except sqlite3.Error as e:
                logger.error(f"Failed to clear long_term_memory: {str(e)}")
                st.error(f"Failed to clear memory: {str(e)}")
            st.session_state.telemetry_data.clear()
            st.success("Memory and telemetry cleared!")

    st.title("VOTSai Advanced Research Platform")
    st.markdown("Your AI-powered research companion.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Query", "Code Analysis", "Directory & Git", "Documentation", "Telemetry & Report"])

    with tab1:
        query = st.text_area("Enter your research query:", height=150, 
                             placeholder="e.g., 'crawl https://example.com', 'explain quantum computing', or 'recall <keyword>'")
        col1, col2 = st.columns([3, 1])
        with col2:
            st.session_state.share_format = st.selectbox("Share Format", ["Text", "Markdown", "JSON"], 
                                                         index=["Text", "Markdown", "JSON"].index(st.session_state.share_format))
        
        if st.button("Execute Query", key="query_btn"):
            if query:
                with st.spinner("Processing..."):
                    processed_query, is_crawl = preprocess_query(query)
                    # Force Local DeepSeek if selected, otherwise use model factory logic
                    if st.session_state.selected_model == "Local DeepSeek":
                        model = model_factory.create_model("Local DeepSeek")
                    else:
                        model = model_factory.select_model(processed_query, st.session_state.selected_model, st.session_state.web_priority, intent_classifier)
                    temperature = 0.1 + (st.session_state.creativity_level / 100) * 0.9
                    for attempt in range(2):
                        try:
                            result = asyncio.run(orchestrate_query(
                                query=processed_query,
                                timeout=st.session_state.timeout,
                                short_term_memory=st.session_state.short_term_memory,
                                conn=conn,
                                model=model,
                                web_priority=st.session_state.web_priority if st.session_state.selected_model != "Local DeepSeek" else False,
                                temperature=temperature,
                                share_format=st.session_state.share_format
                            ))
                            break
                        except Exception as e:
                            logger.error(f"Query attempt {attempt + 1} failed: {str(e)}")
                            if attempt == 1:
                                st.error(f"Query processing failed after retries: {str(e)}")
                                result = {"final_answer": f"Error: {str(e)}", "model_name": st.session_state.selected_model, 
                                          "latency": 0, "actions": 1, "model_reasoning": "Query failure"}
                    if "final_answer" in result:
                        memory_context = get_relevant_memory(conn, processed_query)
                        refined_answer = analyze_response_with_r1(result["final_answer"], processed_query, memory_context, is_crawl=is_crawl)
                        st.markdown(refined_answer)
                        if result["final_answer"] == "No relevant memory found.":
                            st.info("No matching memory entries found.")
                        elif "failed" in result["final_answer"].lower():
                            st.warning("Initial query execution encountered issues; displaying best effort response.")
                        st.write(f"**Metadata**: Model: {result['model_name']}, Latency: {result['latency']:.2f}s, "
                                 f"Actions: {result['actions']}, Reasoning: {result['model_reasoning']}")
                        result["timestamp"] = datetime.datetime.now().isoformat()
                        result["model"] = result["model_name"]
                        result["answer"] = refined_answer
                        telemetry_entry = {
                            "timestamp": result["timestamp"],
                            "query": processed_query,
                            "latency": result["latency"],
                            "model": result["model_name"],
                            "input_tokens": result.get("input_tokens", 0),
                            "output_tokens": result.get("output_tokens", len(refined_answer.split()) if refined_answer else 0)
                        }
                        st.session_state.telemetry_data.append(telemetry_entry)
                        update_memory(conn, processed_query, result, st.session_state.short_term_memory)
                        if "save the script as" in processed_query.lower():
                            try:
                                script_name = processed_query.lower().split("save the script as")[1].split("'")[1]
                                with open(script_name, "w", encoding="utf-8") as f:
                                    script_content = refined_answer.split("**Analysis**")[0].strip() if "**Analysis**" in refined_answer else refined_answer
                                    f.write(script_content)
                                st.info(f"Script saved as '{script_name}'")
                            except (IndexError, IOError) as e:
                                st.error(f"Failed to save script: {str(e)}")
                                logger.error(f"Script save failed: {str(e)}")
                        st.success(f"Completed in {result['latency']:.2f}s")
                    else:
                        st.error("Query failed to produce a valid response. Check logs for details.")
            else:
                st.warning("Please enter a query.")
        
        if st.checkbox("Show Recent Memory"):
            if st.session_state.short_term_memory:
                st.subheader("Recent Queries")
                seen_queries = set()
                for i, entry in enumerate(reversed(st.session_state.short_term_memory), 1):
                    if "timestamp" not in entry:
                        entry["timestamp"] = datetime.datetime.now().isoformat()
                    query_key = (entry["query"], entry["timestamp"])
                    if query_key not in seen_queries:
                        seen_queries.add(query_key)
                        st.write(f"{i}. **Query**: {entry['query']} | **Answer**: {entry['answer'][:100] + '...' if len(entry['answer']) > 100 else entry['answer']} | **Timestamp**: {entry['timestamp']}")
            else:
                st.info("Short-term memory is empty.")

    with tab2:
        code_input = st.text_area("Enter code to analyze:", height=150, placeholder="e.g., 'def add(a, b): return a + b'")
        if st.button("Analyze Code", key="code_btn"):
            if code_input:
                with st.spinner("Analyzing..."):
                    analysis = asyncio.run(analyze_code(code_input))
                    st.markdown(f"**Analysis Result:**\n{analysis}")
            else:
                st.warning("Please enter code to analyze.")

    with tab3:
        st.subheader("Directory Contents & Git Assistance")
        dir_contents = get_directory_contents()
        st.text_area("Current Directory (~VOTSai):", value=dir_contents, height=150, disabled=True)
        
        git_query = st.text_input("Ask Local DeepSeek for Git or Improvement Help:", 
                                  placeholder="e.g., 'suggest a commit message' or 'improve app.py'")
        if st.button("Ask Local DeepSeek", key="git_btn"):
            if git_query:
                with st.spinner("Processing with Local DeepSeek..."):
                    model = model_factory.create_model("Local DeepSeek")
                    full_query = f"Directory contents:\n{dir_contents}\n\nUser query: {git_query}"
                    result = asyncio.run(model.query(
                        query=full_query,
                        timeout=st.session_state.timeout,
                        memory_context=get_relevant_memory(conn, git_query),
                        temperature=0.1 + (st.session_state.creativity_level / 100) * 0.9
                    ))
                    st.markdown(f"**Local DeepSeek Response:**\n{result['answer']}")
                    st.write(f"**Metadata**: Latency: {result.get('latency', 0):.2f}s, Input Tokens: {result['input_tokens']}, Output Tokens: {result['output_tokens']}")
                    result["timestamp"] = datetime.datetime.now().isoformat()
                    result["model"] = "Local DeepSeek"
                    update_memory(conn, git_query, result, st.session_state.short_term_memory)

    with tab4:
        st.header("Documentation")
        try:
            with open("README.md", "r") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("README.md not found.")
        
        st.header("System Documentation")
        try:
            with open("SYSTEM_DOCUMENTATION.md", "r") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("SYSTEM_DOCUMENTATION.md not found.")

    with tab5:
        st.header("Telemetry & Report")
        
        st.subheader("Query Telemetry")
        if st.session_state.telemetry_data:
            df = pd.DataFrame(st.session_state.telemetry_data)
            latency_chart = alt.Chart(df).mark_line().encode(
                x=alt.X("timestamp:T", title="Time"),
                y=alt.Y("latency:Q", title="Latency (s)"),
                color="model:N",
                tooltip=["timestamp", "query", "latency", "model", "input_tokens", "output_tokens"]
            ).properties(title="Query Latency Over Time").interactive()
            st.altair_chart(latency_chart, use_container_width=True)
        else:
            st.info("No telemetry data available yet. Run some queries to see visualizations.")
        
        st.subheader(f"Daily Report - {datetime.datetime.now().date()}")
        report_df = generate_daily_report(conn, st.session_state.short_term_memory)
        if not report_df.empty:
            st.dataframe(report_df)
            st.write("**Summary:**")
            st.write(f"Total Queries: {len(report_df)}")
            st.write(f"Average Latency: {report_df['Latency'].mean():.2f}s")
            st.write(f"Total Input Tokens: {report_df['Input Tokens'].sum()}")
            st.write(f"Total Output Tokens: {report_df['Output Tokens'].sum()}")
        else:
            st.info("No queries recorded for today.")

    # Cyberpunk footer on all tabs
    st.markdown('<div class="cyberpunk-footer">Powered by <a href="https://www.villageofthousands.io/" target="_blank">https://www.villageofthousands.io/</a></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()