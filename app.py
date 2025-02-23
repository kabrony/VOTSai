import streamlit as st
import asyncio
import os
import subprocess
from collections import deque
from core.models import ModelFactory
from core.memory import init_memory_db, update_memory, get_relevant_memory
from core.classifier import IntentClassifier
from handlers.query import orchestrate_query
from utils.constants import SHORT_TERM_MAX
from agents.codeAgent import analyze_code
import logging

logging.basicConfig(filename="vots_agi.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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
        st.error("⚠️ Missing API keys. Set PERPLEXITY_API_KEY and DEEPSEEK_API_KEY in .env.")
        return False
    return True

def get_directory_contents():
    """Return contents of ~/VOTSai directory as a string."""
    dir_path = os.getcwd()
    contents = os.listdir(dir_path)
    return "\n".join([f"- {item}" + (" (dir)" if os.path.isdir(os.path.join(dir_path, item)) else "") for item in contents])

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

    if not load_env():
        return

    conn = init_memory_db("vots_agi_memory.db")
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
            st.success("Memory cleared!")

    st.title("VOTSai Advanced Research Platform")
    st.markdown("Your AI-powered research companion.")

    tab1, tab2, tab3, tab4 = st.tabs(["Query", "Code Analysis", "Directory & Git", "Documentation"])

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
                    model = model_factory.select_model(query, st.session_state.selected_model, st.session_state.web_priority, intent_classifier)
                    temperature = 0.1 + (st.session_state.creativity_level / 100) * 0.9
                    result = asyncio.run(orchestrate_query(
                        query=query,
                        timeout=st.session_state.timeout,
                        short_term_memory=st.session_state.short_term_memory,
                        conn=conn,
                        model=model,
                        web_priority=st.session_state.web_priority,
                        temperature=temperature,
                        share_format=st.session_state.share_format
                    ))
                    if "final_answer" in result:
                        st.markdown(result["final_answer"])
                        if result["final_answer"] == "No relevant memory found.":
                            st.info("No matching memory entries found. Try a different keyword or run some queries first.")
                        st.write(f"**Metadata**: Model: {result['model_name']}, Latency: {result['latency']:.2f}s, "
                                 f"Actions: {result['actions']}, Reasoning: {result['model_reasoning']}")
                        st.success(f"Completed in {result['latency']:.2f}s")
                    else:
                        st.error("Query failed. Check logs for details.")
            else:
                st.warning("Please enter a query.")
        
        # Optional: Show recent memory entries
        if st.checkbox("Show Recent Memory"):
            if st.session_state.short_term_memory:
                st.subheader("Recent Queries")
                for i, entry in enumerate(st.session_state.short_term_memory, 1):
                    st.write(f"{i}. **Query**: {entry['query']} | **Answer**: {entry['answer'][:50]}...")
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
                    update_memory(conn, git_query, result, st.session_state.short_term_memory)
            else:
                st.warning("Please enter a query.")

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

if __name__ == "__main__":
    main()