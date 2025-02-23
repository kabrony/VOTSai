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

logging.basicConfig(filename="vots_agi.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Custom SQLite adapter for datetime to avoid deprecation warning
def adapt_datetime(dt):
    """Convert Python datetime to ISO format string for SQLite."""
    return dt.isoformat()

sqlite3.register_adapter(datetime.datetime, adapt_datetime)

def load_env():
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
    """Preprocess the query to ensure valid URL format for crawl commands."""
    query = query.strip()
    if query.lower().startswith("crawl "):
        url = query[6:].strip()
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("file://") or url.startswith("raw:")):
            query = f"crawl https://{url}"
            st.info(f"Added 'https://' to URL: {query}")
            logger.info(f"Preprocessed query: {query}")
    # Add CoT and deep research instruction
    query = f"{query} [Use chain-of-thought reasoning and deep research style to generate a detailed, creative response up to the maximum token limit]"
    return query

def get_directory_contents():
    """Return contents of ~/VOTSai directory as a string."""
    dir_path = os.getcwd()
    contents = os.listdir(dir_path)
    return "\n".join([f"- {item}" + (" (dir)" if os.path.isdir(os.path.join(dir_path, item)) else "") for item in contents])

def update_database_schema(conn):
    """Update the long_term_memory table schema to include all required columns."""
    c = conn.cursor()
    c.execute("PRAGMA table_info(long_term_memory)")
    columns = [col[1] for col in c.fetchall()]
    
    if "model" not in columns:
        c.execute("ALTER TABLE long_term_memory ADD COLUMN model TEXT")
    if "latency" not in columns:
        c.execute("ALTER TABLE long_term_memory ADD COLUMN latency REAL")
    if "input_tokens" not in columns:
        c.execute("ALTER TABLE long_term_memory ADD COLUMN input_tokens INTEGER")
    if "output_tokens" not in columns:
        c.execute("ALTER TABLE long_term_memory ADD COLUMN output_tokens INTEGER")
    
    conn.commit()

def generate_daily_report(conn, short_term_memory):
    """Generate a daily report of queries and results."""
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
    
    c = conn.cursor()
    c.execute("SELECT timestamp, query, answer, model, latency, input_tokens, output_tokens FROM long_term_memory WHERE DATE(timestamp) = ?", (today_str,))
    for row in c.fetchall():
        report_data["Timestamp"].append(row[0])
        report_data["Query"].append(row[1])
        report_data["Result"].append(row[2][:100] + "..." if len(row[2]) > 100 else row[2])
        report_data["Model"].append(row[3] if row[3] is not None else "Unknown")
        report_data["Latency"].append(row[4] if row[4] is not None else 0)
        report_data["Input Tokens"].append(row[5] if row[5] is not None else 0)
        report_data["Output Tokens"].append(row[6] if row[6] is not None else 0)
    
    return pd.DataFrame(report_data)

def main():
    st.set_page_config(page_title="VOTSai V1.4.4", layout="wide", initial_sidebar_state="expanded", page_icon="🧠")
    
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
        st.session_state.telemetry_data = []

    if not load_env():
        return

    if not ensure_playwright_installed():
        return

    conn = init_memory_db("vots_agi_memory.db")
    update_database_schema(conn)
    model_factory = ModelFactory()
    intent_classifier = IntentClassifier()

    with st.sidebar:
        st.header("⚙️ AI Configuration")
        model_options = ["Auto", "Perplexity API", "DeepSeek API", "Local DeepSeek"]
        st.session_state.selected_model = st.selectbox("Model Selection", model_options, index=model_options.index(st.session_state.selected_model))
        st.session_state.web_priority = st.toggle("🌐 Web Integration", value=st.session_state.web_priority)
        st.session_state.creativity_level = st.slider("🧠 Creativity Level", 0, 100, st.session_state.creativity_level)
        st.session_state.timeout = st.slider("Timeout (s)", 10, 120, st.session_state.timeout)
        if st.button("Clear Memory"):
            st.session_state.short_term_memory.clear()
            conn.execute("DELETE FROM long_term_memory")
            conn.commit()
            st.session_state.telemetry_data = []
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
                    processed_query = preprocess_query(query)
                    model = model_factory.select_model(processed_query, st.session_state.selected_model, st.session_state.web_priority, intent_classifier)
                    temperature = 0.1 + (st.session_state.creativity_level / 100) * 0.9
                    for attempt in range(2):  # Retry once if API fails
                        try:
                            result = asyncio.run(orchestrate_query(
                                query=processed_query,
                                timeout=st.session_state.timeout,
                                short_term_memory=st.session_state.short_term_memory,
                                conn=conn,
                                model=model,
                                web_priority=st.session_state.web_priority,
                                temperature=temperature,
                                share_format=st.session_state.share_format
                            ))
                            break
                        except Exception as e:
                            logger.error(f"Query attempt {attempt + 1} failed: {str(e)}")
                            if attempt == 1:
                                st.error(f"Failed to process query after retries: {str(e)}")
                                result = {"final_answer": f"Error: Query processing failed - {str(e)}", 
                                          "model_name": st.session_state.selected_model, 
                                          "latency": 0, "actions": 1, "model_reasoning": "Query failure"}
                    if "final_answer" in result:
                        st.markdown(result["final_answer"])
                        if result["final_answer"] == "No relevant memory found.":
                            st.info("No matching memory entries found. Try a different keyword or run some queries first.")
                        elif "failed" in result["final_answer"].lower():
                            st.error("Query execution failed. Check logs or try a simpler query.")
                        st.write(f"**Metadata**: Model: {result['model_name']}, Latency: {result['latency']:.2f}s, "
                                 f"Actions: {result['actions']}, Reasoning: {result['model_reasoning']}")
                        result["timestamp"] = datetime.datetime.now().isoformat()
                        result["model"] = result["model_name"]
                        telemetry_entry = {
                            "timestamp": result["timestamp"],
                            "query": processed_query,
                            "latency": result["latency"],
                            "model": result["model_name"],
                            "input_tokens": result.get("input_tokens", 0),
                            "output_tokens": result.get("output_tokens", 0)
                        }
                        st.session_state.telemetry_data.append(telemetry_entry)
                        update_memory(conn, processed_query, result, st.session_state.short_term_memory)
                        st.success(f"Completed in {result['latency']:.2f}s")
                    else:
                        st.error("Query failed. Check logs for details.")
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
                readme_content = f.read()
            st.markdown(readme_content, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("README.md not found.")
        
        st.header("System Documentation")
        try:
            with open("SYSTEM_DOCUMENTATION.md", "r") as f:
                system_doc_content = f.read()
            st.markdown(system_doc_content, unsafe_allow_html=True)
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

if __name__ == "__main__":
    main()