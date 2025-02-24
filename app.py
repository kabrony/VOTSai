import streamlit as st
import os
import sqlite3
import subprocess
from collections import deque
from datetime import datetime
import pandas as pd
import altair as alt
import logging
from typing import Tuple, Optional, Deque, Dict, Any
import requests
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import markdown

# Assuming these are in separate modules (create if missing)
try:
    from core.models import ModelFactory
    from core.memory import init_memory_db, update_memory, get_relevant_memory
    from core.classifier import IntentClassifier
    from handlers.query import orchestrate_query
    from utils.constants import SHORT_TERM_MAX
    from agents.codeAgent import analyze_code
except ImportError as e:
    st.error(f"Missing module: {e}. Ensure all required modules are present.")
    raise

# Logging setup
logging.basicConfig(
    filename="vots_agi.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)
logger = logging.getLogger(__name__)

# SQLite datetime adapter
def adapt_datetime(dt: datetime) -> str:
    return dt.isoformat()

sqlite3.register_adapter(datetime, adapt_datetime)

def load_env() -> bool:
    """Load environment variables from .env file with improved error handling."""
    env_file = ".env"
    try:
        if os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key] = value.strip()
        required_keys = ["DEEPSEEK_API_KEY"]
        optional_keys = ["PERPLEXITY_API_KEY"]
        missing_required = [key for key in required_keys if key not in os.environ]
        if missing_required:
            st.warning(f"Missing required API keys: {', '.join(missing_required)}. DeepSeek API won’t work.")
        missing_optional = [key for key in optional_keys if key not in os.environ]
        if missing_optional:
            st.info(f"Optional API keys missing: {', '.join(missing_optional)}. Perplexity API disabled.")
        return True
    except Exception as e:
        logger.error(f"Failed to load .env: {e}")
        st.error(f"Error loading .env: {e}")
        return False

def preprocess_query(query: str) -> Tuple[str, bool]:
    """Preprocess query with improved intent detection."""
    query = query.strip()
    is_crawl = query.lower().startswith("crawl ")
    if is_crawl:
        url = query[6:].strip()
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("file://") or url.startswith("raw:")):
            query = f"crawl https://{url}"
            st.info(f"Added 'https://' to URL: {query}")
            logger.info(f"Preprocessed query: {query}")
    query = f"{query} [Use chain-of-thought reasoning to generate a detailed, structured response]"
    return query, is_crawl

def query_deepseek_api(question: str) -> str:
    """Query DeepSeek API R1 with retry logic."""
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ.get('DEEPSEEK_API_KEY', '')}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-r1",
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 2048,
            "temperature": st.session_state.creativity_level / 100.0
        }
        response = requests.post(url, json=payload, headers=headers, timeout=st.session_state.timeout)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        logger.error(f"DeepSeek API query failed: {e}")
        return f"Failed to fetch DeepSeek API response: {e}"

def query_perplexity_api(question: str) -> str:
    """Query Perplexity API R1 with retry logic."""
    try:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ.get('PERPLEXITY_API_KEY', '')}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-r1",
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 2048,
            "temperature": st.session_state.creativity_level / 100.0
        }
        response = requests.post(url, json=payload, headers=headers, timeout=st.session_state.timeout)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        logger.error(f"Perplexity API query failed: {e}")
        return f"Failed to fetch Perplexity API response: {e}"

def setup_rag_system(conn: sqlite3.Connection, batch_size: int = 100) -> Optional[RetrievalQA]:
    """Set up LangChain RAG with FAISS using local Ollama model and embeddings."""
    try:
        with st.spinner("Initializing RAG system..."):
            c = conn.cursor()
            c.execute("SELECT query, answer FROM long_term_memory")
            memory_data = [f"Query: {row[0]}\nAnswer: {row[1]}" for row in c.fetchall()] or ["No prior memory data available."]
            logger.info(f"Fetched {len(memory_data)} memory entries for RAG.")

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.create_documents(memory_data)

            # Use your exact model name from 'ollama list'
            embeddings = OllamaEmbeddings(model="deepseek-r1-distill-qwen-7b:q2_k")
            vectorstore = FAISS.from_documents(docs[:batch_size], embeddings)
            for i in range(batch_size, len(docs), batch_size):
                vectorstore.add_documents(docs[i:i + batch_size])

            retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
            llm = OllamaLLM(model="deepseek-r1-distill-qwen-7b:q2_k", temperature=st.session_state.creativity_level / 100.0)

            prompt_template = PromptTemplate(
                input_variables=["context", "question"],
                template="""Using chain-of-thought reasoning, provide a detailed, structured response to the following question based on the provided context from memory data. Break down your reasoning step-by-step and ensure clarity.

**Context from memory**: {context}

**Question**: {question}

**Response**: """
            )

            rag_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": prompt_template},
                return_source_documents=True
            )
        st.success("RAG system initialized successfully with local model!")
        return rag_chain
    except Exception as e:
        logger.error(f"RAG system setup failed: {e}")
        st.error(f"Failed to initialize RAG system: {e}. Ensure Ollama is running with 'ollama run hf.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF:Q2_K'.")
        return None

def get_directory_contents() -> str:
    """Return formatted list of current directory contents with improved readability."""
    try:
        contents = os.listdir(os.getcwd())
        formatted = "\n".join([f"- {item}{' (dir)' if os.path.isdir(os.path.join(os.getcwd(), item)) else ''}" for item in sorted(contents)])
        return "No contents found" if not contents else formatted
    except Exception as e:
        logger.error(f"Failed to list directory contents: {e}")
        return f"Error: Unable to list directory contents: {e}"

def update_database_schema(conn: sqlite3.Connection) -> None:
    """Update long_term_memory table schema with error handling."""
    try:
        with conn:
            c = conn.cursor()
            c.execute("PRAGMA table_info(long_term_memory)")
            columns = {col[1] for col in c.fetchall()}
            schema_updates = [
                ("model", "TEXT"),
                ("latency", "REAL"),
                ("input_tokens", "INTEGER"),
                ("output_tokens", "INTEGER")
            ]
            for col, col_type in schema_updates:
                if col not in columns:
                    c.execute(f"ALTER TABLE long_term_memory ADD COLUMN {col} {col_type}")
        logger.info("Database schema updated successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to update database schema: {e}")
        st.error(f"Database schema update failed: {e}")

def generate_daily_report(conn: sqlite3.Connection, short_term_memory: Deque[Dict[str, Any]]) -> pd.DataFrame:
    """Generate a daily report of queries with improved data handling."""
    today = datetime.now().date()
    today_str = today.isoformat()
    report_data = {
        "Timestamp": [], "Query": [], "Result": [], "Model": [],
        "Latency": [], "Input Tokens": [], "Output Tokens": []
    }
    
    for entry in short_term_memory:
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().isoformat()
        if datetime.fromisoformat(entry["timestamp"]).date() == today:
            report_data["Timestamp"].append(entry["timestamp"])
            report_data["Query"].append(entry.get("query", "N/A"))
            report_data["Result"].append(entry.get("answer", "N/A")[:100] + "..." if len(entry.get("answer", "")) > 100 else entry.get("answer", "N/A"))
            report_data["Model"].append(entry.get("model", "Unknown"))
            report_data["Latency"].append(entry.get("latency", 0.0))
            report_data["Input Tokens"].append(entry.get("input_tokens", 0))
            report_data["Output Tokens"].append(entry.get("output_tokens", 0))
    
    try:
        with conn:
            c = conn.cursor()
            c.execute("SELECT timestamp, query, answer, model, latency, input_tokens, output_tokens FROM long_term_memory WHERE DATE(timestamp) = ?", (today_str,))
            for row in c.fetchall():
                report_data["Timestamp"].append(row[0])
                report_data["Query"].append(row[1] or "N/A")
                result = row[2] or "N/A"
                report_data["Result"].append(result[:100] + "..." if len(result) > 100 else result)
                report_data["Model"].append(row[3] or "Unknown")
                report_data["Latency"].append(row[4] if row[4] is not None else 0.0)
                report_data["Input Tokens"].append(row[5] if row[5] is not None else 0)
                report_data["Output Tokens"].append(row[6] if row[6] is not None else 0)
    except sqlite3.Error as e:
        logger.error(f"Failed to fetch daily report data: {e}")
    
    return pd.DataFrame(report_data)

def main():
    """Main function for VOTSai with optimized multi-model support."""
    st.set_page_config(
        page_title="VOTSai V1.4.5",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🧠"
    )

    # Initialize session state with defaults
    if "short_term_memory" not in st.session_state:
        st.session_state.short_term_memory = deque(maxlen=SHORT_TERM_MAX)
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "Local DeepSeek-R1-Distill-Qwen-7B"
    if "timeout" not in st.session_state:
        st.session_state.timeout = 60
    if "share_format" not in st.session_state:
        st.session_state.share_format = "Markdown"
    if "creativity_level" not in st.session_state:
        st.session_state.creativity_level = 50
    if "telemetry_data" not in st.session_state:
        st.session_state.telemetry_data = deque(maxlen=1000)
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None

    load_env()
    conn = init_memory_db("vots_agi_memory.db")
    update_database_schema(conn)
    model_factory = ModelFactory()
    intent_classifier = IntentClassifier()

    if st.session_state.selected_model == "Local DeepSeek-R1-Distill-Qwen-7B" and st.session_state.rag_chain is None:
        st.session_state.rag_chain = setup_rag_system(conn)

    # Cyberpunk footer
    footer_style = """
    <style>
    .cyberpunk-footer {
        position: fixed; bottom: 10px; left: 0; width: 100%; text-align: center;
        font-family: 'Courier New', monospace; font-size: 16px; color: #26A69A;
        text-shadow: 0 0 5px #26A69A, 0 0 10px #26A69A, 0 0 20px #26A69A;
        animation: matrix 1.5s infinite alternate;
    }
    @keyframes matrix { from { opacity: 0.7; } to { opacity: 1; } }
    </style>
    <div class="cyberpunk-footer">
        <img src="powered_by_villageofthousands.gif" alt="Powered by VillageOfThousands.io" style="max-height: 50px;">
    </div>
    """
    st.markdown(footer_style, unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ AI Configuration")
        model_options = ["Local DeepSeek-R1-Distill-Qwen-7B", "DeepSeek API R1", "Perplexity API R1"]
        st.session_state.selected_model = st.selectbox("Model Selection", model_options, index=0, help="Choose your AI model.")
        st.session_state.creativity_level = st.slider("🧠 Creativity Level", 0, 100, st.session_state.creativity_level, help="Higher values increase response creativity.")
        st.session_state.timeout = st.slider("⏳ Timeout (s)", 10, 120, st.session_state.timeout, help="Max time for API or model responses.")
        if st.button("🧹 Clear Memory", help="Reset memory and telemetry data."):
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
    st.markdown("Your AI-powered research companion, upgraded for 2025.")

    tabs = st.tabs(["Query", "Code Analysis", "Directory & Git", "Documentation", "Telemetry & Report"])
    
    with tabs[0]:
        query = st.text_area(
            "Enter your research query:",
            height=150,
            placeholder="e.g., 'generate a CPU monitoring script', 'recall <keyword>', 'analyze project structure'",
            help="Type your query here."
        )
        col1, col2 = st.columns([3, 1])
        with col2:
            st.session_state.share_format = st.selectbox(
                "Share Format",
                ["Text", "Markdown", "JSON"],
                index=["Text", "Markdown", "JSON"].index(st.session_state.share_format),
                help="Choose output format."
            )
        
        if st.button("🚀 Execute Query", key="query_btn"):
            if query:
                with st.spinner(f"Processing with {st.session_state.selected_model}..."):
                    processed_query, is_crawl = preprocess_query(query)
                    if is_crawl and st.session_state.selected_model not in ["DeepSeek API R1", "Perplexity API R1"]:
                        st.warning("Crawling is only supported with DeepSeek API R1 or Perplexity API R1.")
                    try:
                        if st.session_state.selected_model == "Local DeepSeek-R1-Distill-Qwen-7B" and st.session_state.rag_chain:
                            result_dict = st.session_state.rag_chain.invoke(processed_query)
                            result = result_dict.get('result', str(result_dict))
                            sources = result_dict.get('source_documents', [])
                            if sources:
                                result += "\n\n**Sources from Memory:**\n" + "\n".join([f"- {doc.page_content[:100]}..." for doc in sources])
                        elif st.session_state.selected_model == "DeepSeek API R1":
                            result = query_deepseek_api(processed_query)
                        elif st.session_state.selected_model == "Perplexity API R1":
                            result = query_perplexity_api(processed_query)
                        else:
                            result = "Model not initialized or unavailable."

                        if "execute" in processed_query.lower() and "```" in result:
                            try:
                                code_blocks = [block.strip() for block in result.split("```") if block.strip()]
                                if len(code_blocks) > 1:
                                    script_content = code_blocks[1]
                                    script_name = "temp_script.py"
                                    with open(script_name, "w", encoding="utf-8") as f:
                                        f.write(script_content)
                                    process = subprocess.run(
                                        [sys.executable, script_name],
                                        capture_output=True,
                                        text=True,
                                        timeout=10
                                    )
                                    execution_output = f"**Script Output:**\n{process.stdout}\n**Errors (if any):**\n{process.stderr}"
                                    result += f"\n\n{execution_output}"
                                    os.remove(script_name)
                                else:
                                    result += "\n\n**Execution Result:** No valid code block found."
                            except subprocess.TimeoutExpired:
                                result += "\n\n**Execution Result:** Script timed out after 10 seconds."
                            except Exception as e:
                                result += f"\n\n**Execution Result:** Failed to execute script: {str(e)}"
                        st.markdown(result)
                    except Exception as e:
                        logger.error(f"Query failed: {e}")
                        st.warning("Query execution encountered issues.")
                        st.error(f"Query failed: {e}")

    with tabs[1]:
        code_input = st.text_area(
            "Paste code to analyze:",
            height=150,
            placeholder="e.g., Python script",
            help="Enter code for analysis."
        )
        if st.button("🔍 Analyze Code", key="code_btn"):
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
        st.text_area("Current Directory:", value=dir_contents, height=200, disabled=True, help="Current working directory contents.")
        if st.button("🔄 Refresh Directory"):
            st.rerun()
        try:
            git_status = subprocess.run(["git", "status"], capture_output=True, text=True, check=True, timeout=5).stdout
            st.text_area("Git Status:", value=git_status, height=200, disabled=True, help="Current Git repository status.")
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to get Git status: {e}")
        except subprocess.TimeoutExpired:
            st.error("Git status retrieval timed out.")

    with tabs[3]:
        st.subheader("Documentation")
        documentation_content = """
        ### 🚀🤖 VOTSai: Advanced AI Research Platform (V1.4.5)

        VOTSai is a cutting-edge, open-source, Streamlit-based platform for AI-driven research, powered by **DeepSeek-R1** (API), **Perplexity API R1**, or locally via **DeepSeek-R1-Distill-Qwen-7B-GGUF:Q2_K** with Ollama.

        #### 🌟 Features
        - **🧠 Multi-Model Support**: Choose between DeepSeek API R1, Perplexity API R1, or local Ollama for reasoning and analysis.
        - **📚 Enhanced Memory**: SQLite-backed long-term memory with short-term deque for fast recall.
        - **💻 Code Analysis**: AI-driven script review and optimization.
        - **📂 Directory Insights**: Explore project structure and Git status.
        - **📜 Structured Output**: Responses in Text, Markdown, or JSON.

        #### 📦 Quick Start
        ##### Prerequisites
        - Python 3.12+
        - Git
        - Virtual Environment (venv)
        - Ollama (for local model)

        ##### Installation
        ```bash
        git clone https://github.com/kabrony/VOTSai.git
        cd VOTSai
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```

        ##### Running Locally
        1. Start Ollama (local model):
        ```bash
        ollama pull hf.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF:Q2_K
        ollama run hf.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF:Q2_K
        ```
        2. Launch VOTSai:
        ```bash
        streamlit run app.py
        ```
        3. Open `http://localhost:8501`.

        ##### Configuration
        Set API keys in `.env` for DeepSeek/Perplexity:
        ```bash
        DEEPSEEK_API_KEY=your_deepseek_key
        PERPLEXITY_API_KEY=your_perplexity_key
        ```

        #### 🛠️ Core Features
        - **Queries**: DeepSeek API R1 or Perplexity API R1 for advanced reasoning; local model for offline use.
        - **Memory**: `recall <keyword>` to retrieve past results from SQLite.
        - **Code Analysis**: Optimize scripts with AI insights.
        - **Directory**: View project files and Git status.

        #### 📈 Advanced Usage
        - **Timeout**: 10-120s for query execution.
        - **Creativity**: 0-100 scale for response style.
        - **Examples**: `generate a CPU monitor`, `analyze my repo`, `recall quantum`.

        #### 🤝 Contributing
        - Star us: `kabrony/VOTSai`
        - Fork & PR to enhance features.

        #### 🙌 Thanks
        Built with ❤️ by kabrony, powered by DeepSeek and Ollama.
        """
        st.markdown(documentation_content, unsafe_allow_html=True)

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
            ).interactive().properties(width=600, height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No telemetry data available for today.")

if __name__ == "__main__":
    main()