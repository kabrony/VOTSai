import streamlit as st
import asyncio
import os
import sys
import sqlite3
import subprocess
from collections import deque
from datetime import datetime
import pandas as pd
import altair as alt
import logging
from typing import Tuple, Optional, Deque, Dict, Any
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
import requests
import markdown

# Assuming these are in separate modules (create if missing)
from core.models import ModelFactory
from core.memory import init_memory_db, update_memory, get_relevant_memory
from core.classifier import IntentClassifier
from handlers.query import orchestrate_query
from utils.constants import SHORT_TERM_MAX
from agents.codeAgent import analyze_code

# Logging setup
logging.basicConfig(filename="vots_agi.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# SQLite datetime adapter
def adapt_datetime(dt: datetime) -> str:
    return dt.isoformat()

sqlite3.register_adapter(datetime, adapt_datetime)

def load_env() -> bool:
    """Load environment variables from .env file."""
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
    required_keys = ["PERPLEXITY_API_KEY", "DEEPSEEK_API_KEY", "HUGGINGFACE_API_TOKEN"]
    missing = [key for key in required_keys if key not in os.environ]
    if missing:
        st.error(f"⚠️ Missing API keys: {', '.join(missing)}. Set them in .env or Streamlit secrets.")
        return False
    return True

def ensure_playwright_installed() -> bool:
    """Verify Playwright is installed and browsers are available."""
    try:
        import playwright
    except ImportError:
        st.error("Playwright module not found. Ensure 'playwright>=1.50.0' is in requirements.txt and installed.")
        logger.error("Playwright module not installed.")
        return False
    playwright_dir = os.path.expanduser("~/.cache/ms-playwright")
    if not os.path.exists(playwright_dir) or not os.path.isdir(os.path.join(playwright_dir, "chromium")):
        st.error("Playwright browsers not installed. Run 'python -m playwright install chromium'.")
        logger.error("Playwright browsers not found.")
        return False
    return True

def preprocess_query(query: str) -> Tuple[str, bool]:
    """Preprocess query and detect crawl intent."""
    query = query.strip()
    is_crawl = query.lower().startswith("crawl ")
    if is_crawl:
        url = query[6:].strip()
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("file://") or url.startswith("raw:")):
            query = f"crawl https://{url}"
            st.info(f"Added 'https://' to URL: {query}")
            logger.info(f"Preprocessed query: {query}")
    query = f"{query} [Use chain-of-thought reasoning and deep research style to generate a detailed, creative response]"
    return query, is_crawl

def query_perplexity(question: str) -> str:
    """Query Perplexity API for additional context."""
    try:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {"Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}", "Content-Type": "application/json"}
        payload = {
            "model": "mistral-7b-instruct",
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 1024
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Perplexity API query failed: {str(e)}")
        return f"Failed to fetch Perplexity context: {str(e)}"

def setup_rag_system(conn: sqlite3.Connection, batch_size: int = 100) -> Optional[RetrievalQA]:
    """Set up LangChain RAG with FAISS and SQLite memory using batch processing."""
    try:
        with st.spinner("Initializing RAG system..."):
            c = conn.cursor()
            c.execute("SELECT query, answer FROM long_term_memory")
            memory_data = [f"Query: {row[0]}\nAnswer: {row[1]}" for row in c.fetchall()] or ["No prior memory data available."]
            logger.info(f"Fetched {len(memory_data)} memory entries for RAG.")

            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = text_splitter.create_documents(memory_data)

            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = None
            for i in range(0, len(docs), batch_size):
                batch = docs[i:i + batch_size]
                if vectorstore is None:
                    vectorstore = FAISS.from_documents(batch, embeddings)
                else:
                    vectorstore.add_documents(batch)

            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            llm = HuggingFaceHub(
                repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
                huggingfacehub_api_token=os.environ["HUGGINGFACE_API_TOKEN"],
                model_kwargs={"temperature": 0.1}
            )

            prompt_template = PromptTemplate(
                input_variables=["context", "question"],
                template="""Using chain-of-thought reasoning, generate a detailed, creative response to the following question based on the provided context from memory data and additional research if applicable.

Context from memory: {context}

Question: {question}

Response:"""
            )

            rag_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": prompt_template}
            )
        st.success("RAG system initialized successfully!")
        return rag_chain
    except Exception as e:
        logger.error(f"RAG system setup failed: {e}")
        st.error(f"Failed to initialize RAG system: {e}")
        return None

def get_directory_contents() -> str:
    """Return formatted list of current directory contents."""
    try:
        contents = os.listdir(os.getcwd())
        return "\n".join([f"- {item}" + (" (dir)" if os.path.isdir(os.path.join(os.getcwd(), item)) else "") for item in contents])
    except Exception as e:
        logger.error(f"Failed to list directory contents: {e}")
        return f"Error: Unable to list directory contents: {e}"

def update_database_schema(conn: sqlite3.Connection) -> None:
    """Update long_term_memory table schema if needed."""
    try:
        with conn:
            c = conn.cursor()
            c.execute("PRAGMA table_info(long_term_memory)")
            columns = {col[1] for col in c.fetchall()}
            for col, col_type in [("model", "TEXT"), ("latency", "REAL"), ("input_tokens", "INTEGER"), ("output_tokens", "INTEGER")]:
                if col not in columns:
                    c.execute(f"ALTER TABLE long_term_memory ADD COLUMN {col} {col_type}")
        logger.info("Database schema updated successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to update database schema: {e}")
        st.error(f"Database schema update failed: {e}")

def generate_daily_report(conn: sqlite3.Connection, short_term_memory: Deque[Dict[str, Any]]) -> pd.DataFrame:
    """Generate a daily report of queries from memory."""
    today = datetime.now().date()
    today_str = today.isoformat()
    report_data = {"Timestamp": [], "Query": [], "Result": [], "Model": [], "Latency": [], "Input Tokens": [], "Output Tokens": []}
    
    for entry in short_term_memory:
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().isoformat()
        if datetime.fromisoformat(entry["timestamp"]).date() == today:
            report_data["Timestamp"].append(entry["timestamp"])
            report_data["Query"].append(entry["query"])
            report_data["Result"].append(entry["answer"][:100] + "..." if len(entry["answer"]) > 100 else entry["answer"])
            report_data["Model"].append(entry.get("model", "Unknown"))
            report_data["Latency"].append(entry.get("latency", 0))
            report_data["Input Tokens"].append(entry.get("input_tokens", 0))
            report_data["Output Tokens"].append(entry.get("output_tokens", 0))
    
    try:
        with conn:
            c = conn.cursor()
            c.execute("SELECT timestamp, query, answer, model, latency, input_tokens, output_tokens FROM long_term_memory WHERE DATE(timestamp) = ?", (today_str,))
            for row in c.fetchall():
                report_data["Timestamp"].append(row[0])
                report_data["Query"].append(row[1])
                report_data["Result"].append(row[2][:100] + "..." if len(row[2]) > 100 else row[2])
                report_data["Model"].append(row[3] or "Unknown")
                report_data["Latency"].append(row[4] if row[4] is not None else 0)
                report_data["Input Tokens"].append(row[5] if row[5] is not None else 0)
                report_data["Output Tokens"].append(row[6] if row[6] is not None else 0)
    except sqlite3.Error as e:
        logger.error(f"Failed to fetch daily report data: {e}")
    
    return pd.DataFrame(report_data)

def main():
    """Main function for VOTSai application with enhanced LangChain RAG integration."""
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
        st.session_state.telemetry_data = deque(maxlen=1000)
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None

    if not load_env() or not ensure_playwright_installed():
        return

    conn = init_memory_db("vots_agi_memory.db")
    update_database_schema(conn)
    model_factory = ModelFactory()
    intent_classifier = IntentClassifier()

    if st.session_state.rag_chain is None:
        st.session_state.rag_chain = setup_rag_system(conn)

    # Cyberpunk footer with VillageOfThousands branding
    footer_style = """
    <style>
    .cyberpunk-footer {
        position: fixed; bottom: 10px; left: 0; width: 100%; text-align: center;
        font-family: 'Courier New', monospace; font-size: 16px; color: #26A69A;
        text-shadow: 0 0 5px #26A69A, 0 0 10px #26A69A, 0 0 20px #26A69A;
        animation: matrix 1.5s infinite alternate;
    }
    @keyframes matrix { from { opacity: 0.7; } to { opacity: 1; } }
    .cyberpunk-footer a { color: #4DD0E1; text-decoration: none; }
    .cyberpunk-footer a:hover { text-shadow: 0 0 10px #4DD0E1, 0 0 20px #4DD0E1, 0 0 30px #4DD0E1; }
    </style>
    <div class="cyberpunk-footer">
        Powered by <a href="https://VillageOfThousands.io" target="_blank">VillageOfThousands.io</a>
    </div>
    """
    st.markdown(footer_style, unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ AI Configuration")
        model_options = ["Auto", "Perplexity API", "DeepSeek API", "Cloud LLM"]
        st.session_state.selected_model = st.selectbox("Model Selection", model_options, index=model_options.index(st.session_state.selected_model))
        st.session_state.web_priority = st.toggle("🌐 Web Integration", value=st.session_state.web_priority)
        st.session_state.creativity_level = st.slider("🧠 Creativity Level", 0, 100, st.session_state.creativity_level)
        st.session_state.timeout = st.slider("Timeout (s)", 10, 120, st.session_state.timeout)
        if st.button("Clear Memory"):
            try:
                with conn:
                    conn.execute("DELETE FROM long_term_memory")
                st.session_state.short_term_memory.clear()
                st.session_state.telemetry_data.clear()
                st.session_state.rag_chain = None
                st.success("Memory and telemetry cleared!")
            except sqlite3.Error as e:
                logger.error(f"Failed to clear memory: {e}")
                st.error(f"Failed to clear memory: {e}")

    st.title("VOTSai Advanced Research Platform")
    st.markdown("Your AI-powered research companion with LangChain RAG.")

    tabs = st.tabs(["Query", "Code Analysis", "Directory & Git", "Documentation", "Telemetry & Report"])
    
    with tabs[0]:
        query = st.text_area("Enter your research query:", height=150, placeholder="e.g., 'crawl https://example.com', 'generate a CPU monitoring script', or 'recall <keyword>'")
        col1, col2 = st.columns([3, 1])
        with col2:
            st.session_state.share_format = st.selectbox("Share Format", ["Text", "Markdown", "JSON"], index=["Text", "Markdown", "JSON"].index(st.session_state.share_format))
        
        if st.button("Execute Query", key="query_btn"):
            if query:
                with st.spinner("Processing with LangChain RAG..."):
                    processed_query, is_crawl = preprocess_query(query)
                    if st.session_state.rag_chain:
                        try:
                            if is_crawl and st.session_state.web_priority:
                                perplexity_context = query_perplexity(processed_query.split(" [")[0])
                            else:
                                perplexity_context = ""
                            result_dict = st.session_state.rag_chain.invoke(processed_query + (f"\nAdditional Web Context: {perplexity_context}" if is_crawl else ""))
                            result = result_dict.get('result', str(result_dict))
                            if "execute" in processed_query.lower() and "```" in result:
                                try:
                                    code_blocks = result.split("```")
                                    if len(code_blocks) > 1:
                                        script_content = code_blocks[1].strip()
                                        script_name = "temp_script.py"
                                        with open(script_name, "w", encoding="utf-8") as f:
                                            f.write(script_content)
                                        process = subprocess.run(
                                            [sys.executable, script_name],
                                            capture_output=True,
                                            text=True,
                                            timeout=10
                                        )
                                        execution_output = f"Script Output:\n{process.stdout}\nErrors (if any):\n{process.stderr}"
                                        result += f"\n\n**Execution Result:**\n{execution_output}"
                                        os.remove(script_name)
                                    else:
                                        result += "\n\n**Execution Result:** No valid code block found."
                                except subprocess.TimeoutExpired:
                                    result += "\n\n**Execution Result:** Script timed out after 10 seconds."
                                except Exception as e:
                                    result += f"\n\n**Execution Result:** Failed to execute script: {str(e)}"
                            st.markdown(result)
                        except Exception as e:
                            logger.error(f"RAG query failed: {e}")
                            st.warning("Initial query execution encountered issues; displaying best effort response.")
                            st.error(f"Query failed: {e}")
                    else:
                        st.error("RAG system not initialized. Please check setup.")

    with tabs[1]:
        code_input = st.text_area("Paste code to analyze:", height=150, placeholder="e.g., Python script")
        if st.button("Analyze Code", key="code_btn"):
            if code_input:
                with st.spinner("Analyzing code..."):
                    try:
                        analysis = analyze_code(code_input)
                        st.markdown(analysis)
                    except Exception as e:
                        logger.error(f"Code analysis failed: {e}")
                        st.error(f"Code analysis failed: {e}")

    with tabs[2]:
        st.subheader("Directory Contents & Git Status")
        dir_contents = get_directory_contents()
        st.text_area("Current Directory:", value=dir_contents, height=200, disabled=True)
        if st.button("Refresh Directory"):
            st.rerun()
        try:
            git_status = subprocess.run(["git", "status"], capture_output=True, text=True, check=True).stdout
            st.text_area("Git Status:", value=git_status, height=200, disabled=True)
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to get Git status: {e}")

    with tabs[3]:
        st.subheader("Documentation")
        st.markdown("### VOTSai Documentation\n\nYour AI-powered research companion.\n\n- **Query**: Ask questions or crawl websites.\n- **Code Analysis**: Analyze and optimize scripts.\n- **Directory & Git**: View project structure and Git status.\n- **Telemetry**: Monitor query performance.")

    with tabs[4]:
        st.subheader("Telemetry & Daily Report")
        report_df = generate_daily_report(conn, st.session_state.short_term_memory)
        if not report_df.empty:
            st.dataframe(report_df, use_container_width=True)
            chart = alt.Chart(report_df).mark_line().encode(
                x="Timestamp:T",
                y="Latency:Q",
                color="Model:N",
                tooltip=["Query", "Result", "Latency", "Input Tokens", "Output Tokens"]
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No telemetry data available for today.")

if __name__ == "__main__":
    main()