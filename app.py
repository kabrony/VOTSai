from calendar import month_name
import streamlit as st
import asyncio
import os
import sys
import sqlite3
import subprocess
import requests
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
from langchain.embeddings import HuggingFaceEmbeddings  # Cloud-compatible embeddings
from langchain_ollama import OllamaLLM
import markdown

# Modular imports (assuming these are in separate files)
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
    if "PERPLEXITY_API_KEY" not in os.environ or "DEEPSEEK_API_KEY" not in os.environ:
        st.error("⚠️ Missing API keys. Set PERPLEXITY_API_KEY and DEEPSEEK_API_KEY in .env or Streamlit secrets.")
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
    query = f"{query} [Use chain-of-thought reasoning and deep research style to generate a detailed, creative response up to the maximum token limit]"
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
    """Set up LangChain RAG with FAISS, DeepSeek R1, and SQLite memory using batch processing."""
    try:
        with st.spinner("Setting up RAG system..."):
            c = conn.cursor()
            c.execute("SELECT query, answer FROM long_term_memory")
            memory_data = [f"Query: {row[0]}\nAnswer: {row[1]}" for row in c.fetchall()] or ["No prior memory data available."]
            logger.info(f"Fetched {len(memory_data)} memory entries for RAG.")

            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = text_splitter.create_documents(memory_data)

            # Use HuggingFaceEmbeddings for cloud compatibility
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = None
            for i in range(0, len(docs), batch_size):
                batch = docs[i:i + batch_size]
                if vectorstore is None:
                    vectorstore = FAISS.from_documents(batch, embeddings)
                else:
                    vectorstore.add_documents(batch)

            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            llm = OllamaLLM(model="hf.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF:Q2_K", temperature=0.1)

            prompt_template = PromptTemplate(
                input_variables=["context", "question"],
                template="""Using chain-of-thought reasoning, generate a detailed, creative response to the following question based on the provided context from memory data and additional research if applicable. If the question involves a web crawl, enhance the description with insights about the website’s purpose, structure, and features. If it involves code, generate an improved script with robust error handling and performance optimizations. Include a detailed analysis section.

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
        return rag_chain
    except Exception as e:
        logger.error(f"RAG system setup failed: {e}")
        st.error(f"Failed to initialize RAG system: {e}")
        return None

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
    model_factory = ModelFactory()
    intent_classifier = IntentClassifier()

    if st.session_state.rag_chain is None:
        st.session_state.rag_chain = setup_rag_system(conn)

    with st.sidebar:
        st.header("⚙️ AI Configuration")
        model_options = ["Auto", "Perplexity API", "DeepSeek API", "Local DeepSeek"]
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
                            if is_crawl:
                                perplexity_context = query_perplexity(processed_query.split(" [")[0])
                            else:
                                perplexity_context = ""
                            result_dict = st.session_state.rag_chain.invoke(processed_query + (f"\nAdditional Web Context: {perplexity_context}" if is_crawl else ""))
                            result = result_dict.get('result', str(result_dict))
                            st.markdown(result)
                        except Exception as e:
                            logger.error(f"RAG query failed: {e}")
                            st.error(f"Query failed: {e}")
                    else:
                        st.error("RAG system not initialized.")

if __name__ == "__main__":
    main()              st.warning("Initial query execution encountered issues; displaying best effort response.")
                    st.write(f"**Metadata**: Model: {month_name}, Latency: {latency:.2f}s, Actions: {actions}, Reasoning: {reasoning}")
                    result_entry = {
                        "timestamp": datetime.datetime.now().isoformat(),
                        "query": processed_query,
                        "answer": result,
                        "model": model_name,
                        "latency": latency,
                        "actions": actions,
                        "model_reasoning": reasoning,
                        "input_tokens": 0,
                        "output_tokens": len(result.split()) if result else 0
                    }
                    st.session_state.telemetry_data.append(result_entry)
                    update_memory(conn, processed_query, result_entry, st.session_state.short_term_memory)
                    if "save the script as" in processed_query.lower():
                        try:
                            script_name = processed_query.lower().split("save the script as")[1].split("'")[1]
                            with open(script_name, "w", encoding="utf-8") as f:
                                script_content = result.split("**Analysis**")[0].strip() if "**Analysis**" in result else result
                                f.write(script_content)
                            st.info(f"Script saved as '{script_name}'")
                        except (IndexError, IOError) as e:
                            st.error(f"Failed to save script: {e}")
                            logger.error(f"Script save failed: {e}")
                    st.success(f"Completed in {latency:.2f}s")
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

    with tabs[1]:
        code_input = st.text_area("Enter code to analyze:", height=150, placeholder="e.g., 'def add(a, b): return a + b'")
        if st.button("Analyze Code", key="code_btn"):
            if code_input:
                with st.spinner("Analyzing..."):
                    analysis = asyncio.run(analyze_code(code_input))
                    st.markdown(f"**Analysis Result:**\n{analysis}")
            else:
                st.warning("Please enter code to analyze.")

    with tabs[2]:
        st.subheader("Directory Contents & Git Assistance")
        dir_contents = get_directory_contents()
        st.text_area("Current Directory (~VOTSai):", value=dir_contents, height=150, disabled=True)
        
        git_query = st.text_input("Ask Local DeepSeek for Git or Improvement Help:", placeholder="e.g., 'suggest a commit message' or 'improve app.py'")
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

    with tabs[3]:
        st.header("Documentation")
        # Load custom CSS for Documentation tab
        try:
            with open("docs/docs/styles/custom.css", "r") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Custom CSS file not found at 'docs/docs/styles/custom.css'.")
            logger.error("Custom CSS file not found at 'docs/docs/styles/custom.css'.")

        # Load index.md as primary documentation
        try:
            with open("docs/docs/index.md", "r") as f:
                md_content = f.read()
                html_content = markdown.markdown(md_content, extensions=['pymdownx.highlight', 'pymdownx.superfences', 'md_in_html'])
                st.markdown(html_content, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Documentation file not found at 'docs/docs/index.md'.")
            logger.error("Documentation file not found at 'docs/docs/index.md'.")

        # Add footer image matching Markdown with error handling
        footer_html = (
            '<div class="md-footer-custom">'
            '<img src="docs/docs/assets/powered_by_villageofthousands.gif" alt="Powered by Village of Thousands">'
            '</div>'
        )
        try:
            if os.path.exists("docs/docs/assets/powered_by_villageofthousands.gif"):
                st.markdown(footer_html, unsafe_allow_html=True)
            else:
                st.warning("Footer image not found at 'docs/docs/assets/powered_by_villageofthousands.gif'. Please add it.")
                logger.warning("Footer image not found at 'docs/docs/assets/powered_by_villageofthousands.gif'.")
        except Exception as e:
            st.error(f"Failed to load footer image: {str(e)}")
            logger.error(f"Failed to load footer image: {str(e)}")

    with tabs[4]:
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

    # Footer displayed on all tabs except Documentation (where it's custom)
    st.markdown('<div class="cyberpunk-footer">Powered by <a href="https://www.villageofthousands.io/" target="_blank">https://www.villageofthousands.io/</a></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()