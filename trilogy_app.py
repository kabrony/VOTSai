import streamlit as st
import time
import pandas as pd
import json
import re
from datetime import datetime
from trilogy_integration import process_query
from core.version_control import VersionControl
from matrix_terminal import MatrixTerminal
import pickle
import os
import base64
from pygments import highlight
from pygments.lexers import get_lexer_by_name, Python3Lexer, guess_lexer
from pygments.formatters import HtmlFormatter

# Set page config FIRST - must be the first st command
st.set_page_config(
    page_title="TRILOGY Brain - Matrix Interface",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize version control
version_control = VersionControl()

# Create the Matrix terminal instance AFTER set_page_config
matrix_terminal = MatrixTerminal(initialize_now=False)  # Don't initialize yet

# Modified state initialization for persistent chat history
if "messages" not in st.session_state:
    # Try to load from disk
    try:
        with open('chat_history.pkl', 'rb') as f:
            st.session_state.messages = pickle.load(f)
    except FileNotFoundError:
        st.session_state.messages = []

# Initialize session state
if "telemetry" not in st.session_state:
    st.session_state.telemetry = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "model_override" not in st.session_state:
    st.session_state.model_override = "Auto (TRILOGY Brain)"
if "thinking_depth" not in st.session_state:
    st.session_state.thinking_depth = 0.7
if "show_metadata" not in st.session_state:
    st.session_state.show_metadata = False
if "last_update_check" not in st.session_state:
    st.session_state.last_update_check = time.time()

# Apply theme CSS
theme_css = """
<style>
    /* Base Theme */
    .stApp {
        transition: background-color 0.5s ease;
    }
    
    /* Dark Theme (Default) */
    .dark-theme .stApp {
        background-color: #121212;
        color: #f0f0f0;
    }
    .dark-theme .stMarkdown, .dark-theme p, .dark-theme h1, .dark-theme h2, .dark-theme h3 {
        color: #f0f0f0;
    }
    .dark-theme .stButton button {
        background-color: #2c2c2c;
        color: #ffffff;
        border: 1px solid #555;
        border-radius: 5px;
    }
    .dark-theme .stTextInput input, .dark-theme .stTextArea textarea {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444;
        border-radius: 5px;
    }
    .dark-theme h1, .dark-theme h2, .dark-theme h3 {
        color: #9e9eff;
    }
    .dark-theme .stTabs [data-baseweb="tab-list"] {
        background-color: #1e1e1e;
    }
    .dark-theme .stTabs [data-baseweb="tab"] {
        color: #f0f0f0;
    }
    
    /* Light Theme */
    .light-theme .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    .light-theme .stMarkdown, .light-theme p, .light-theme h1, .light-theme h2, .light-theme h3 {
        color: #333333;
    }
    .light-theme .stButton button {
        background-color: #f0f0f0;
        color: #333333;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .light-theme .stTextInput input, .light-theme .stTextArea textarea {
        background-color: #f9f9f9;
        color: #333333;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .light-theme h1, .light-theme h2, .light-theme h3 {
        color: #5252b5;
    }
    .light-theme .stTabs [data-baseweb="tab-list"] {
        background-color: #f9f9f9;
    }
    .light-theme .stTabs [data-baseweb="tab"] {
        color: #333333;
    }
    
    /* Chat Message Styling */
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        position: relative;
    }
    .chat-message.user {
        background-color: rgba(120, 120, 250, 0.1);
    }
    .chat-message.assistant {
        background-color: rgba(250, 250, 250, 0.1);
    }
    .message-metadata {
        font-size: 0.8em;
        color: #888;
        text-align: right;
        margin-top: 5px;
    }
    
    /* Code Block Styling */
    pre {
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
    }
    code {
        font-family: 'Courier New', monospace;
    }
    
    /* Thinking Process Styling */
    .thinking-process {
        background-color: rgba(100, 100, 100, 0.1);
        padding: 10px;
        border-left: 3px solid #9e9eff;
        margin: 10px 0;
        border-radius: 0 5px 5px 0;
    }
    
    /* Animation for thinking */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    .thinking-animation {
        animation: pulse 1.5s infinite;
    }
    
    /* React buttons */
    .react-button {
        background: transparent;
        border: none;
        font-size: 1.2em;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .react-button:hover {
        transform: scale(1.2);
    }
</style>
"""

# Apply the theme
st.markdown(theme_css, unsafe_allow_html=True)
st.markdown(f'<div class="{st.session_state.theme}-theme"></div>', unsafe_allow_html=True)

# Add this line to initialize Matrix terminal
matrix_terminal.initialize()

# Display the VOTSai ASCII header with Village of Thousands link
matrix_terminal.display_votsai_header()

# Make Matrix theme default
st.markdown("""
<style>
/* Global Orange Terminal Theme */
body {
    background-color: #000 !important;
    color: #FF9C00 !important;  /* Changed from green to orange */
    font-family: 'Courier New', monospace !important;
}

.stApp {
    background-color: #000 !important;
}

.stSidebar {
    background-color: #000 !important;
    border-right: 1px solid #FF9C00 !important;  /* Changed color */
}

/* Text elements */
* {
    color: #FF9C00 !important;  /* Changed color */
}

h1, h2, h3, h4, h5, h6 {
    color: #FF9C00 !important;  /* Changed color */
    text-shadow: 0 0 5px #A85F00 !important;  /* Reduced glow */
}

p {
    color: #00FF00 !important;
}

/* Input elements */
input, textarea, select, .stTextInput input, .stTextArea textarea {
    background-color: #000 !important;
    color: #00FF00 !important;
    border: 1px solid #00FF00 !important;
    border-radius: 3px !important;
}

/* Button elements */
button, .stButton button {
    background-color: #000 !important;
    color: #FF9C00 !important;  /* Changed color */
    border: 1px solid #FF9C00 !important;  /* Changed color */
    box-shadow: 0 0 5px #A85F00 !important;  /* Reduced glow */
}

button:hover, .stButton button:hover {
    background-color: #003000 !important;
    border: 1px solid #00FF00 !important;
    box-shadow: 0 0 10px #00FF00 !important;
}

/* Cards and containers */
.stCard {
    background-color: #001000 !important;
    border: 1px solid #00FF00 !important;
    box-shadow: 0 0 10px #00FF00 !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: #000 !important;
    border-bottom: 1px solid #00FF00 !important;
}

.stTabs [data-baseweb="tab"] {
    color: #00FF00 !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #00FF00 !important;
    border-bottom: 2px solid #00FF00 !important;
    box-shadow: 0 0 5px #00FF00 !important;
}

/* Chat messages */
.stChatMessage {
    background-color: #001500 !important;
    border: 1px solid #00AA00 !important;
}

/* Dataframes */
.dataframe {
    color: #00FF00 !important;
    background-color: #001000 !important;
}

.dataframe th {
    background-color: #002000 !important;
    color: #00FF00 !important;
}

/* Progress bar */
.stProgress > div > div {
    background-color: #00FF00 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #001000 !important;
    color: #00FF00 !important;
}

/* Code blocks */
pre {
    background-color: #001500 !important;
    border: 1px solid #00AA00 !important;
}

code {
    color: #00FF00 !important;
}

/* Animation for page transitions */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.stApp {
    animation: fadeIn 1s ease-in;
}

/* Matrix logo animation */
@keyframes pulse {
    0% { text-shadow: 0 0 5px #00FF00; }
    50% { text-shadow: 0 0 15px #00FF00, 0 0 25px #00FF00; }
    100% { text-shadow: 0 0 5px #00FF00; }
}

.matrix-logo {
    animation: pulse 2s infinite;
}
</style>
""", unsafe_allow_html=True)

# Replace the current header with Matrix header
st.markdown("""
<h1 class="matrix-logo" style="text-align: center; font-family: 'Courier New', monospace; 
font-weight: bold; color: #00FF00; text-shadow: 0 0 10px #00FF00;">
THE MATRIX • TRILOGY BRAIN</h1>
<p style="text-align: center; color: #00AA00;">Neural Interface v{}</p>
""".format(version_control.get_current_version()), unsafe_allow_html=True)

# Main app
st.title("🧠 VOTSai with TRILOGY Brain")
st.markdown(f"<p>Advanced AI assistant powered by the TRILOGY Brain architecture • <strong>{version_control.get_current_version()}</strong></p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <h2 style="color:#00FF00; text-shadow: 0 0 5px #00FF00;">COMMAND CENTER</h2>
    """, unsafe_allow_html=True)
    
    # Model selection
    st.subheader("AGENT SELECTION")
    
    # Helper function to convert between naming schemes
    def convert_to_matrix_name(standard_name):
        if "TRILOGY Brain" in standard_name:
            return standard_name.replace("TRILOGY Brain", "TRILOGY Core")
        return standard_name.replace(" API", " Node").replace(" DeepSeek", " Node")

    # Model selection with proper name conversion
    matrix_options = ["Auto (TRILOGY Core)", "Claude Node", "DeepSeek Node", "Perplexity Node", "Local Node"]
    standard_options = ["Auto (TRILOGY Brain)", "Claude API", "DeepSeek API", "Perplexity API", "Local DeepSeek"]

    # Find the current value in matrix format
    current_matrix_name = convert_to_matrix_name(st.session_state.model_override)
    current_index = 0  # Default to first option
    for i, name in enumerate(matrix_options):
        if name.lower() == current_matrix_name.lower():
            current_index = i
            break

    # Display the dropdown with matrix names
    selected_matrix_name = st.selectbox(
        "Neural Agent:",
        matrix_options,
        index=current_index
    )

    # Convert back to standard name for internal use
    selected_index = matrix_options.index(selected_matrix_name)
    st.session_state.model_override = standard_options[selected_index]
    
    st.session_state.thinking_depth = st.slider("Processing Depth", 0.0, 1.0, st.session_state.thinking_depth, 
                            help="Controls neural processing intensity")
    
    # Stats section with Matrix terminology
    st.markdown("""<hr style="border-color:#00FF00; opacity:0.5;">""", unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color:#00FF00; text-shadow: 0 0 5px #00FF00;">SYSTEM STATUS</h3>
    """, unsafe_allow_html=True)
    
    # Calculate active models from telemetry with Matrix terms
    active_nodes = set()
    for t in st.session_state.telemetry:
        if "model" in t and t["model"]:
            active_nodes.add(t["model"].replace("API", "Node"))
    
    for node in active_nodes:
        st.markdown(f"<span style='color:#00AA00;'>●</span> {node} <span style='color:#00AA00;'>ACTIVE</span>", unsafe_allow_html=True)
    
    # System control panel
    st.markdown("""<hr style="border-color:#00FF00; opacity:0.5;">""", unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color:#00FF00; text-shadow: 0 0 5px #00FF00;">SYSTEM CONTROLS</h3>
    """, unsafe_allow_html=True)
    
    if st.button("PURGE MEMORY CACHE"):
        st.session_state.messages = []
        st.success("Memory cache purged successfully")
        st.rerun()
        
    if st.button("DEPLOY NEW VERSION"):
        version_type = "patch"
        description = "Matrix Interface Enhancement"
        
        new_version = version_control.create_new_version(
            version_type=version_type,
            description=description
        )
        st.success(f"New system version deployed: {new_version}")
        st.rerun()

# Create tabs
tabs = st.tabs(["Neural Interface", "System Access", "Memory Core", "Diagnostics", "Daily Logs"])

# Main Terminal tab (renamed from "Terminal")
with tabs[0]:
    # Chat container with fixed height to prevent jump on reload
    st.markdown("""
    <style>
    .chat-container {
        height: 600px;
        overflow-y: auto;
        border: 1px solid #333;
        border-radius: 0; /* Square corners for terminal feel */
        padding: 10px;
        margin-bottom: 15px;
        background-color: #000;
    }
    .user-message {
        background-color: #111;
        padding: 10px;
        border-radius: 0;
        margin: 5px 0 15px 50px;
        border-left: 3px solid #444;
    }
    .system-message {
        background-color: #0a0a0a;
        padding: 10px;
        border-radius: 0;
        margin: 5px 50px 15px 0;
        border-left: 3px solid #222;
    }
    .message-header {
        color: #d0d0d0;
        font-size: 0.9em;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
    }
    .thinking-toggle {
        cursor: pointer;
        color: #888;
        font-size: 0.8em;
    }
    .thinking-content {
        background-color: #0a0a0a;
        padding: 10px;
        border-radius: 0;
        margin-top: 10px;
        font-family: monospace;
        font-size: 0.9em;
        border-left: 2px solid #333;
        max-height: 300px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the conversation history
    chat_html = '<div class="chat-container" id="chat-container">'
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            # User message
            chat_html += f"""
            <div class="user-message">
                <div class="message-header">
                    <span>User</span>
                    <span>{datetime.fromtimestamp(msg.get('timestamp', 0)).strftime('%H:%M:%S')}</span>
                </div>
                {msg["content"]}
            </div>
            """
        else:
            # System message
            thinking = msg.get("thinking", "")
            thinking_html = ""
            if thinking:
                thinking_html = f"""
                <div class="thinking-toggle" onclick="toggleThinking(this)">► Show Thinking Process</div>
                <div class="thinking-content" style="display: none;">
                    {thinking}
                </div>
                """
            
            chat_html += f"""
            <div class="system-message">
                <div class="message-header">
                    <span>TRILOGY Brain ({msg.get('metadata', {}).get('model', 'System')})</span>
                    <span>{datetime.fromtimestamp(msg.get('timestamp', 0)).strftime('%H:%M:%S')}</span>
                </div>
                {msg["content"]}
                {thinking_html}
            </div>
            """
    
    chat_html += '</div>'
    
    # Add JavaScript for thinking toggle
    chat_html += """
    <script>
    function toggleThinking(element) {
        var content = element.nextElementSibling;
        if (content.style.display === "none") {
            content.style.display = "block";
            element.innerHTML = "▼ Hide Thinking Process";
        } else {
            content.style.display = "none";
            element.innerHTML = "► Show Thinking Process";
        }
    }
    
    // Scroll to bottom of chat container
    document.addEventListener('DOMContentLoaded', function() {
        var chatContainer = document.getElementById('chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    });
    </script>
    """
    
    st.markdown(chat_html, unsafe_allow_html=True)
    
    # Query input with terminal-style prompt
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 15px;">
        <span class="terminal-prompt">$</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Input box
    query = st.text_input("Terminal", placeholder="Enter your query...", key="matrix_query", label_visibility="collapsed")
    
    if query:
        # Use Oracle for meta-reasoning
        oracle_analysis = oracle.analyze_query(query)
        
        # Check if this is a code-related query
        code_info = oracle.analyze_code_query(query)
        
        # Process any code blocks for analysis
        if code_info["is_code_related"] and code_info["code_blocks"]:
            for lang, code in code_info["code_blocks"]:
                # Default to python if language not specified
                language = lang.lower() if lang else "python"
                
                # Analyze the code
                code_analysis = code_analyzer.analyze_code(code, language)
                
                # Add code analysis to oracle analysis
                oracle_analysis["code_analysis"] = code_analysis
        
        # Add to user message display
        with st.expander("Query Analysis", expanded=False):
            st.json(oracle_analysis)
        
        # Process with enhanced context
        context = {
            "thinking_depth": st.session_state.thinking_depth,
            "oracle_analysis": oracle_analysis,
            "code_info": code_info if code_info["is_code_related"] else None
        }
        
        # Process the query
        with st.status("Processing..."):
            result = process_query(query, context=context)
        
        # Add user message to chat history with metadata
        st.session_state.messages.append({
            "role": "user",
            "content": query,
            "timestamp": time.time()
        })
        
        # Add system response to chat history with code analysis if applicable
        response_content = result["answer"]
        
        # Format code analysis suggestions if this was code-related
        if code_info["is_code_related"] and "code_analysis" in oracle_analysis:
            code_suggestions = code_analyzer.get_improvement_suggestions(oracle_analysis["code_analysis"])
            if code_suggestions:
                suggestion_text = "\n\n**Code Improvement Suggestions:**\n" + "\n".join(code_suggestions)
                response_content += suggestion_text
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_content,
            "metadata": {
                "model": result.get("model", "Unknown"),
                "execution_time": result.get("metadata", {}).get("execution_time", 0),
                "quality_score": result.get("metadata", {}).get("quality_score", 0)
            },
            "thinking": result.get("thinking", ""),
            "timestamp": time.time()
        })
        
        # Save chat history
        save_chat_history()
        
        # Force a rerun to display the updated chat
        st.rerun()

# Add this below the chat UI
st.markdown("<hr style='border-color: #FF9C00; margin: 30px 0;'>", unsafe_allow_html=True)

# Add telemetry dashboard
st.markdown("""
<h3 style="margin-bottom: 20px; color: #e6e6e6; font-weight: 500;">System Telemetry</h3>
""", unsafe_allow_html=True)

# Create columns for telemetry metrics
col1, col2, col3 = st.columns(3)

# Collect telemetry data
if st.session_state.messages:
    assistant_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]
    total_queries = len(assistant_msgs)
    avg_time = sum([m.get("metadata", {}).get("execution_time", 0) for m in assistant_msgs]) / max(1, total_queries)
    models_used = {}
    for m in assistant_msgs:
        model = m.get("metadata", {}).get("model", "Unknown")
        models_used[model] = models_used.get(model, 0) + 1
    
    with col1:
        st.metric("Total Queries", total_queries)
    
    with col2:
        st.metric("Avg. Response Time", f"{avg_time:.2f}s")
    
    with col3:
        # Find most used model
        most_used = max(models_used.items(), key=lambda x: x[1])[0] if models_used else "None"
        st.metric("Primary Model", most_used)
    
    # Show model distribution
    st.subheader("Model Usage")
    model_data = pd.DataFrame(list(models_used.items()), columns=["Model", "Count"])
    st.bar_chart(model_data, x="Model", y="Count")
    
    # Show last few execution details in a compact table
    st.subheader("Recent Executions")
    recent_data = []
    for msg in reversed(assistant_msgs[-5:]):
        meta = msg.get("metadata", {})
        recent_data.append({
            "Time": datetime.fromtimestamp(msg.get("timestamp", 0)).strftime('%Y-%m-%d %H:%M:%S'),
            "Model": meta.get("model", "Unknown"),
            "Execution Time": f"{meta.get('execution_time', 0):.2f}s",
            "Quality Score": f"{meta.get('quality_score', 0):.2f}"
        })
    
    st.table(pd.DataFrame(recent_data))
else:
    st.info("No telemetry data available yet. Start chatting to see insights.")

# Add control buttons for the chat
export_col, clear_col = st.columns(2)

with export_col:
    if st.button("Export Conversation", key="export_chat"):
        # Create exportable text
        export_text = "# TRILOGY Brain Conversation\n\n"
        for msg in st.session_state.messages:
            role = "User" if msg["role"] == "user" else "TRILOGY Brain"
            timestamp = datetime.fromtimestamp(msg.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')
            export_text += f"## {role} ({timestamp})\n\n{msg['content']}\n\n"
        
        # Create a download link
        b64 = base64.b64encode(export_text.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="trilogy_conversation.md">Download Conversation</a>'
        st.markdown(href, unsafe_allow_html=True)

with clear_col:
    if st.button("Clear Conversation", key="clear_chat"):
        st.session_state.messages = []
        save_chat_history()
        st.rerun()

# Classic Chat tab
with tabs[1]:
    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        # Apply custom styling
        if message["role"] == "user":
            message_class = "user"
        else:
            message_class = "assistant"
        
        st.markdown(f'<div class="chat-message {message_class}">', unsafe_allow_html=True)
        
        with st.chat_message(message["role"]):
            # For assistant messages, check if there's thinking to display
            if message["role"] == "assistant" and "thinking" in message:
                with st.expander("**View Thinking Process**", expanded=False):
                    st.markdown(f'<div class="thinking-process">{message["thinking"]}</div>', unsafe_allow_html=True)
            
            # Display the message content with code highlighting
            st.markdown(message["content"], unsafe_allow_html=True)
            
            # Show metadata for assistant messages
            if message["role"] == "assistant" and ("metadata" in message) and (st.session_state.show_metadata or st.button("View Metadata", key=f"metadata_{i}")):
                with st.expander("Response Metadata", expanded=True):
                    st.json(message["metadata"])
            
            # For assistant messages, add reaction buttons
            if message["role"] == "assistant":
                cols = st.columns([1, 1, 1, 7])  # Adjust the column widths
                
                if cols[0].button("👍", key=f"like_{i}"):
                    st.session_state.feedback.append({
                        "message_id": i, 
                        "feedback": "positive",
                        "timestamp": time.time()
                    })
                    st.toast("Thanks for your feedback!")
                
                if cols[1].button("👎", key=f"dislike_{i}"):
                    st.session_state.feedback.append({
                        "message_id": i, 
                        "feedback": "negative",
                        "timestamp": time.time()
                    })
                    st.toast("Thanks for your feedback! We'll try to improve.")
                
                if cols[2].button("🔄", key=f"retry_{i}"):
                    if i > 0 and st.session_state.messages[i-1]["role"] == "user":
                        query = st.session_state.messages[i-1]["content"]
                        st.toast("Regenerating response...")
                        # Use a different model for retry
                        context = {"retry": True, "model_override": "Claude API" if message.get("metadata", {}).get("model") != "Claude API" else "DeepSeek API"}
                        try:
                            result = process_query(query, context=context)
                            # Update the existing message
                            st.session_state.messages[i] = {
                                "role": "assistant",
                                "content": result["answer"],
                                "metadata": result.get("metadata", {}),
                                "timestamp": time.time()
                            }
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error regenerating response: {str(e)}")
                
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": time.time()
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Show thinking animation
            message_placeholder.markdown('<div class="thinking-animation">🧠 Thinking...</div>', unsafe_allow_html=True)
            
            # Prepare context with model override if specified
            context = None
            if st.session_state.model_override != "Auto (TRILOGY Brain)":
                context = {"model_override": st.session_state.model_override.replace(" API", "")}
            
            # Add thinking depth
            if context is None:
                context = {"thinking_depth": st.session_state.thinking_depth}
            else:
                context["thinking_depth"] = st.session_state.thinking_depth
            
            # Process the query through TRILOGY Brain
            try:
                with st.status("Processing with TRILOGY Brain...") as status:
                    st.write("Analyzing query...")
                    start_time = time.time()
                    result = process_query(prompt, context=context)
                    latency = time.time() - start_time
                    model_used = result.get("model", "Unknown")
                    st.write(f"Generating response with {model_used}...")
                    status.update(label="Response Complete", state="complete", expanded=False)
                
                # Update the message
                message_placeholder.markdown(result["answer"], unsafe_allow_html=True)
                
                # Add metadata display
                metadata = result.get("metadata", {})
                metadata["latency"] = latency
                metadata["model"] = result.get("model", "Unknown")
                
                if st.session_state.show_metadata:
                    with st.expander("Response Metadata", expanded=True):
                        st.json(metadata)
                
                # Add to telemetry
                st.session_state.telemetry.append({
                    "query": prompt,
                    "latency": latency,
                    "model": result.get("model", "Unknown"),
                    "execution_time": metadata.get("execution_time", 0),
                    "quality_score": metadata.get("quality_score", 0),
                    "timestamp": time.time()
                })
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                result = {
                    "answer": f"I'm sorry, I encountered an error while processing your request: {str(e)}",
                    "model": "Error",
                    "metadata": {"error": str(e)}
                }
                message_placeholder.markdown(result["answer"])
        
        # Add assistant message to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result["answer"],
            "metadata": metadata if 'metadata' in locals() else {},
            "thinking": result.get("thinking", ""),
            "timestamp": time.time()
        })
        
        # Auto-scroll to bottom
        st.rerun()

# Memory Explorer tab
with tabs[2]:
    st.header("Memory Explorer")
    st.write("Explore the system's memory to see what it has learned")
    
    # Query memory
    memory_query = st.text_input("Search memories:")
    if memory_query and st.button("Search"):
        st.write(f"Searching for memories related to: {memory_query}")
        
        # This is a placeholder - would need to integrate with actual memory system
        results = []
        for message in st.session_state.messages:
            if message["role"] == "assistant" and memory_query.lower() in message["content"].lower():
                results.append(message)
        
        if results:
            st.success(f"Found {len(results)} relevant memories")
            for result in results:
                with st.expander(result["content"][:50] + "..."):
                    st.markdown(result["content"])
                    st.text(f"Timestamp: {datetime.fromtimestamp(result.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.info("No relevant memories found")
    
    # Display recent memories
    st.subheader("Recent Conversations")
    
    # Group messages into conversations
    conversations = []
    current_conversation = []
    
    for message in st.session_state.messages:
        current_conversation.append(message)
        if len(current_conversation) >= 2:  # User + Assistant makes a complete exchange
            if len(current_conversation) % 2 == 0:  # Complete exchange
                conversations.append(current_conversation.copy())
                current_conversation = []
    
    # Add the last incomplete conversation if any
    if current_conversation:
        conversations.append(current_conversation)
    
    # Display conversations
    for i, conversation in enumerate(conversations):
        # Format the title with timestamp if available
        title = f"Conversation {i+1}"
        if "timestamp" in conversation[0]:
            timestamp = datetime.fromtimestamp(conversation[0]["timestamp"]).strftime("%Y-%m-%d %H:%M")
            title += f" - {timestamp}"
        
        with st.expander(title):
            for message in conversation:
                if "timestamp" in message:
                    time_str = datetime.fromtimestamp(message["timestamp"]).strftime("%H:%M:%S")
                    st.markdown(f"**{message['role'].title()}** ({time_str}): {message['content']}")
                else:
                    st.markdown(f"**{message['role'].title()}**: {message['content']}")

# System Info tab
with tabs[3]:
    st.header("System Information")
    
    # Architecture diagram
    st.subheader("TRILOGY Brain Architecture")
    st.markdown("""
    ```
    ┌───────────────────────────────────┐
    │         TRILOGY Brain             │
    │      (Oracle/Architect)           │
    └─────────────────┬─────────────────┘
                      │
    ┌─────────────────┴─────────────────┐
    │                                   │
    ▼                                   ▼
    ┌───────────────┐     ┌───────────────────┐
    │ Router Module │     │ Memory Management │
    └───────┬───────┘     └─────────┬─────────┘
            │                       │
            ▼                       ▼
    ┌───────────────┐     ┌───────────────────┐
    │ Model Manager │     │  Learning Module  │
    └───────┬───────┘     └─────────┬─────────┘
            │                       │
            ▼                       ▼
    ┌───────────────┐     ┌───────────────────┐
    │  Tool Module  │     │ Evaluation System │
    └───────────────┘     └───────────────────┘
    ```
    """)
    
    # Telemetry data
    st.subheader("Telemetry Data")
    if st.session_state.telemetry:
        # Convert to dataframe with proper datetime
        df = pd.DataFrame(st.session_state.telemetry)
        if "timestamp" in df.columns:
            df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
        
        # Show the dataframe
        st.dataframe(df)
        
        # Performance charts
        st.subheader("Performance Analytics")
        
        # Response time chart
        if "latency" in df.columns:
            st.write("#### Response Time Trend")
            if "datetime" in df.columns:
                chart_data = pd.DataFrame({
                    "datetime": df["datetime"],
                    "response_time": df["latency"]
                })
                st.line_chart(chart_data, x="datetime", y="response_time")
            else:
                chart_data = pd.DataFrame({
                    "index": range(len(df)),
                    "response_time": df["latency"]
                })
                st.line_chart(chart_data, x="index", y="response_time")
        
        # Model distribution
        if "model" in df.columns:
            st.write("#### Model Distribution")
            model_counts = df["model"].value_counts().reset_index()
            model_counts.columns = ["model", "count"]
            st.bar_chart(model_counts, x="model", y="count")
        
        # Quality scores if available
        if "quality_score" in df.columns:
            st.write("#### Quality Scores")
            if "datetime" in df.columns:
                quality_data = pd.DataFrame({
                    "datetime": df["datetime"],
                    "quality_score": df["quality_score"]
                })
                st.line_chart(quality_data, x="datetime", y="quality_score")
    else:
        st.info("No telemetry data available yet. Start chatting to generate data.")
    
    # User feedback summary
    st.subheader("User Feedback")
    if st.session_state.feedback:
        positive = sum(1 for f in st.session_state.feedback if f["feedback"] == "positive")
        negative = sum(1 for f in st.session_state.feedback if f["feedback"] == "negative")
        total = len(st.session_state.feedback)
        
        feedback_data = pd.DataFrame({
            "Feedback": ["Positive", "Negative"],
            "Count": [positive, negative]
        })
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Feedback", total)
        with col2:
            st.metric("Positive", f"{positive} ({positive/total*100:.1f}%)" if total > 0 else "0 (0%)")
        with col3:
            st.metric("Negative", f"{negative} ({negative/total*100:.1f}%)" if total > 0 else "0 (0%)")
        
        # Display chart
        st.bar_chart(feedback_data, x="Feedback", y="Count")
    else:
        st.info("No user feedback collected yet.")
    
    # System status
    st.subheader("System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Status")
        st.markdown('<span style="color:green; font-size:24px;">●</span> Online', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Version")
        st.write(f"TRILOGY Brain {version_control.get_current_version()}")
    
    with col3:
        st.markdown("#### Last Updated")
        st.write(datetime.now().strftime("%Y-%m-%d"))
    
    # System health
    st.subheader("System Health")
    
    # Memory usage (placeholder)
    memory_usage = 45  # percent
    st.progress(memory_usage/100, text=f"Memory Usage: {memory_usage}%")
    
    # CPU usage (placeholder)
    cpu_usage = 30  # percent
    st.progress(cpu_usage/100, text=f"CPU Usage: {cpu_usage}%")
    
    # API quota (placeholder)
    api_quota = 75  # percent used
    st.progress(api_quota/100, text=f"API Quota: {api_quota}% used")

# Global Matrix animation
st.markdown("""
<div id="matrix-background" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: -1; pointer-events: none;"></div>
<script>
// Create Matrix background
function createGlobalMatrixEffect() {
    const background = document.getElementById('matrix-background');
    const canvas = document.createElement('canvas');
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    background.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    const characters = "日ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍｦｲｸｺｿﾁﾄﾉﾌﾔﾖﾙﾚﾛﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    
    // Set canvas size
    function updateCanvasSize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    updateCanvasSize();
    window.addEventListener('resize', updateCanvasSize);
    
    const fontSize = 16;
    const columns = Math.floor(canvas.width / fontSize);
    
    const drops = [];
    for (let i = 0; i < columns; i++) {
        drops[i] = Math.floor(Math.random() * -canvas.height / fontSize);
    }
    
    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        for (let i = 0; i < drops.length; i++) {
            const opacity = Math.random() * 0.2 + 0.1;  // Reduced opacity
            const brightness = Math.floor(Math.random() * 20) + 50;  // Lower brightness
            
            // Orange color (R, G, B)
            ctx.fillStyle = `rgba(${brightness + 155}, ${brightness + 40}, 0, ${opacity})`;
            
            const text = characters[Math.floor(Math.random() * characters.length)];
            ctx.font = `${fontSize}px monospace`;
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    
    setInterval(draw, 50);
}

// Initialize the effect when the DOM is loaded
document.addEventListener('DOMContentLoaded', createGlobalMatrixEffect);
// Also try to initialize right away
setTimeout(createGlobalMatrixEffect, 500);
</script>
""", unsafe_allow_html=True)

# Show splash screen for first-time visitors
if "shown_splash" not in st.session_state:
    matrix_terminal.splash_screen()
    st.session_state.shown_splash = True

# Add this function before it's called
def save_chat_history():
    with open('chat_history.pkl', 'wb') as f:
        pickle.dump(st.session_state.messages, f)

# Updated high-contrast terminal theme - add this after initializing Matrix terminal
st.markdown("""
<style>
/* Professional Dark Terminal Theme (Crawl4AI inspired) */
body {
    background-color: #1a1a1a !important;
    color: #d8d8d8 !important;
    font-family: 'Consolas', 'Menlo', 'Monaco', monospace !important;
}

.stApp {
    background-color: #1a1a1a !important;
}

.stSidebar {
    background-color: #242424 !important;
    border-right: 1px solid #333 !important;
}

/* Text elements */
* {
    color: #d8d8d8 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #e6e6e6 !important;
    text-shadow: none !important;
    font-weight: 500 !important;
}

/* Button elements */
button, .stButton button {
    background-color: #2b2b2b !important;
    color: #d8d8d8 !important;
    border: 1px solid #444 !important;
    box-shadow: none !important;
    border-radius: 3px !important;
    transition: all 0.2s ease;
}

button:hover, .stButton button:hover {
    background-color: #333 !important;
    border: 1px solid #555 !important;
}

/* Input elements */
.stTextInput input, .stTextArea textarea {
    background-color: #2b2b2b !important;
    color: #d8d8d8 !important;
    border: 1px solid #444 !important;
    border-radius: 3px !important;
}

/* Remove default Streamlit styling */
.element-container {
    background-color: #1a1a1a !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: #242424 !important;
    border-bottom: 1px solid #333 !important;
}

.stTabs [data-baseweb="tab"] {
    color: #bbb !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #e6e6e6 !important;
    border-bottom: 2px solid #4c8daa !important;
}

/* Chat container styling */
.chat-container {
    height: 600px;
    overflow-y: auto;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 15px;
    background-color: #242424;
}

.user-message {
    background-color: #2b2b2b;
    padding: 12px;
    border-radius: 4px;
    margin: 8px 0 15px 40px;
    border-left: 3px solid #4c8daa;
}

.system-message {
    background-color: #242424;
    padding: 12px;
    border-radius: 4px;
    margin: 8px 40px 15px 0;
    border-left: 3px solid #555;
}

.message-header {
    color: #bbb;
    font-size: 0.9em;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
}

.thinking-toggle {
    cursor: pointer;
    color: #888;
    font-size: 0.8em;
    padding: 3px 8px;
    border-radius: 3px;
    background-color: #2b2b2b;
    transition: background-color 0.2s ease;
}

.thinking-toggle:hover {
    background-color: #333;
}

.thinking-content {
    background-color: #2b2b2b;
    padding: 12px;
    border-radius: 4px;
    margin-top: 10px;
    font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
    font-size: 0.9em;
    border-left: 2px solid #444;
    max-height: 300px;
    overflow-y: auto;
}

/* Progress bars */
.stProgress > div > div {
    background-color: #4c8daa !important;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    color: #4c8daa !important;
    font-weight: 500 !important;
}

/* Card styling */
.dashboard-card {
    background-color: #242424 !important;
    border: 1px solid #333 !important;
    border-radius: 4px !important;
    padding: 15px !important;
    margin-bottom: 15px !important;
}

/* Terminal prompt styling */
.terminal-prompt {
    color: #4c8daa !important;
    font-family: 'Consolas', 'Menlo', 'Monaco', monospace !important;
    margin-right: 8px !important;
}

/* Table styling */
.stTable {
    border: 1px solid #444 !important;
}

.stTable thead tr th {
    background-color: #242424 !important;
    color: #bbb !important;
    border-bottom: 1px solid #444 !important;
}

.stTable tbody tr:nth-child(even) {
    background-color: #2b2b2b !important;
}

/* Link styling */
a {
    color: #4c8daa !important;
    text-decoration: none !important;
}

a:hover {
    text-decoration: underline !important;
}
</style>
""", unsafe_allow_html=True)

# Run the app with: streamlit run trilogy_app.py 

# Add this function to improve reasoning
def enhance_query_with_cot(query):
    """Enhance a query with Chain of Thought prompting"""
    cot_prompt = f"""
For the following query, I need to think step-by-step:

QUERY: {query}

Let me reason through this systematically:
1. First, I'll understand what's being asked
2. Then, consider relevant knowledge domains
3. Next, analyze any assumptions or constraints
4. Finally, formulate a comprehensive answer

Reasoning:
"""
    return cot_prompt

# Oracle/Architect component for meta-reasoning
class OracleArchitect:
    def __init__(self):
        self.daily_logs = []
        
    def analyze_query(self, query):
        """Meta-reasoning about the best approach to a query"""
        # Determine query complexity and best approach
        complexity = len(query.split()) / 10  # Simple heuristic
        domains = self.identify_domains(query)
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "complexity": min(complexity, 1.0),
            "domains": domains,
            "approach": self.determine_approach(complexity, domains)
        }
        
        # Log the analysis
        self.daily_logs.append(analysis)
        return analysis
    
    def identify_domains(self, query):
        """Identify knowledge domains relevant to the query"""
        domains = []
        
        # Simple keyword matching for domains
        if any(word in query.lower() for word in ["python", "code", "function", "programming"]):
            domains.append("programming")
            
        if any(word in query.lower() for word in ["philosophy", "ethics", "moral", "meaning"]):
            domains.append("philosophy")
            
        if any(word in query.lower() for word in ["history", "war", "century", "ancient"]):
            domains.append("history")
            
        if any(word in query.lower() for word in ["math", "calculate", "equation", "formula"]):
            domains.append("mathematics")
            
        if not domains:
            domains.append("general")
            
        return domains
    
    def determine_approach(self, complexity, domains):
        """Determine the best approach based on complexity and domains"""
        approaches = []
        
        if complexity > 0.7:
            approaches.append("break down into sub-problems")
            
        if "programming" in domains:
            approaches.append("use code examples")
            
        if "mathematics" in domains:
            approaches.append("use step-by-step derivation")
            
        if complexity > 0.5:
            approaches.append("chain of thought reasoning")
            
        return approaches
    
    def save_daily_logs(self):
        """Save the daily logs to a JSON file"""
        today = datetime.now().strftime("%Y-%m-%d")
        with open(f"oracle_logs_{today}.json", "w") as f:
            json.dump(self.daily_logs, f, indent=2)
            
    def get_recent_logs(self, limit=10):
        """Get the most recent logs"""
        return self.daily_logs[-limit:] if self.daily_logs else []

    def analyze_code_query(self, query):
        """Analyze if a query is code-related and extract code info"""
        code_info = {
            "is_code_related": False,
            "probable_language": None,
            "code_blocks": [],
            "action_type": None  # Could be 'analyze', 'debug', 'improve', etc.
        }
        
        # Check if query is code-related
        code_keywords = ["code", "function", "bug", "error", "program", "script", 
                        "debug", "fix", "implement", "develop", "algorithm"]
        
        # Check for code-related keywords
        if any(keyword in query.lower() for keyword in code_keywords):
            code_info["is_code_related"] = True
        
        # Extract code blocks
        code_blocks = re.findall(r'```(\w*)\n(.*?)\n```', query, re.DOTALL)
        if code_blocks:
            code_info["is_code_related"] = True
            code_info["code_blocks"] = code_blocks
            
            # Determine language if not specified
            language = code_blocks[0][0] if code_blocks[0][0] else "unknown"
            code_info["probable_language"] = language
        
        # Determine action type
        if "fix" in query.lower() or "debug" in query.lower() or "error" in query.lower():
            code_info["action_type"] = "debug"
        elif "improve" in query.lower() or "optimize" in query.lower() or "better" in query.lower():
            code_info["action_type"] = "improve"
        elif "explain" in query.lower() or "understand" in query.lower():
            code_info["action_type"] = "explain"
        elif "implement" in query.lower() or "create" in query.lower() or "write" in query.lower():
            code_info["action_type"] = "implement"
        else:
            code_info["action_type"] = "analyze"
        
        return code_info

# Initialize the Oracle/Architect
oracle = OracleArchitect()

# Then modify your query processing:
if query:
    # Use Oracle for meta-reasoning
    oracle_analysis = oracle.analyze_query(query)
    
    # Check if this is a code-related query
    code_info = oracle.analyze_code_query(query)
    
    # Process any code blocks for analysis
    if code_info["is_code_related"] and code_info["code_blocks"]:
        for lang, code in code_info["code_blocks"]:
            # Default to python if language not specified
            language = lang.lower() if lang else "python"
            
            # Analyze the code
            code_analysis = code_analyzer.analyze_code(code, language)
            
            # Add code analysis to oracle analysis
            oracle_analysis["code_analysis"] = code_analysis
        
    # Add to user message display
    with st.expander("Query Analysis", expanded=False):
        st.json(oracle_analysis)
        
    # Process with enhanced context
    context = {
        "thinking_depth": st.session_state.thinking_depth,
        "oracle_analysis": oracle_analysis,
        "code_info": code_info if code_info["is_code_related"] else None
    }
    
    # Process the query
    with st.status("Processing..."):
        result = process_query(query, context=context)
    
    # Add user message to chat history with metadata
    st.session_state.messages.append({
        "role": "user",
        "content": query,
        "timestamp": time.time()
    })
    
    # Add system response to chat history with code analysis if applicable
    response_content = result["answer"]
    
    # Format code analysis suggestions if this was code-related
    if code_info["is_code_related"] and "code_analysis" in oracle_analysis:
        code_suggestions = code_analyzer.get_improvement_suggestions(oracle_analysis["code_analysis"])
        if code_suggestions:
            suggestion_text = "\n\n**Code Improvement Suggestions:**\n" + "\n".join(code_suggestions)
            response_content += suggestion_text
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_content,
        "metadata": {
            "model": result.get("model", "Unknown"),
            "execution_time": result.get("metadata", {}).get("execution_time", 0),
            "quality_score": result.get("metadata", {}).get("quality_score", 0)
        },
        "thinking": result.get("thinking", ""),
        "timestamp": time.time()
    })

# Add this function to highlight code blocks in markdown text
def highlight_code(text):
    """Highlight code blocks in markdown text."""
    # Define pattern to match markdown code blocks with language specification
    pattern = r'```(\w+)\n(.*?)\n```'
    
    # Basic check to avoid processing non-string inputs
    if not isinstance(text, str):
        return text
    
    try:
        # Function to replace matched code blocks with highlighted HTML
        def replace_code(match):
            lang, code = match.groups()
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ValueError:
                # Default to Python if language is not recognized
                lexer = Python3Lexer(stripall=True)
            
            formatter = HtmlFormatter(style='monokai')
            highlighted = highlight(code, lexer, formatter)
            return f'<div class="highlight-code">{highlighted}</div>'
        
        # Replace all code blocks in the text
        highlighted_text = re.sub(pattern, replace_code, text, flags=re.DOTALL)
        
        # Also add CSS for the highlighted code
        css = """
        <style>
        .highlight-code {
            margin: 10px 0;
            padding: 10px;
            border-radius: 4px;
            background-color: #272822;
            overflow-x: auto;
        }
        .highlight-code pre {
            margin: 0;
            padding: 0;
            background: transparent !important;
        }
        .highlight-code .hll { background-color: #49483e }
        .highlight-code .c { color: #75715e } /* Comment */
        .highlight-code .err { color: #960050; background-color: #1e0010 } /* Error */
        .highlight-code .k { color: #66d9ef } /* Keyword */
        .highlight-code .l { color: #ae81ff } /* Literal */
        .highlight-code .n { color: #f8f8f2 } /* Name */
        .highlight-code .o { color: #f92672 } /* Operator */
        .highlight-code .p { color: #f8f8f2 } /* Punctuation */
        .highlight-code .s { color: #e6db74 } /* String */
        .highlight-code .na { color: #a6e22e } /* Name.Attribute */
        .highlight-code .nb { color: #f8f8f2 } /* Name.Builtin */
        .highlight-code .nc { color: #a6e22e } /* Name.Class */
        .highlight-code .no { color: #66d9ef } /* Name.Constant */
        .highlight-code .nd { color: #a6e22e } /* Name.Decorator */
        .highlight-code .nf { color: #a6e22e } /* Name.Function */
        </style>
        """
        return css + highlighted_text
    except Exception as e:
        # Fallback if there's any error in highlighting
        return text

# Add this after your OracleArchitect class
class CodeAnalyzer:
    """Analyzes code for improvements and best practices"""
    
    def __init__(self):
        self.analysis_history = []
        self.common_issues = {
            "python": [
                {"pattern": r"except:", "message": "Use specific exceptions instead of bare except"},
                {"pattern": r"print\(", "message": "Consider using logging instead of print for production code"},
                {"pattern": r"global\s+\w+", "message": "Global variables should be avoided when possible"},
                {"pattern": r"from\s+\w+\s+import\s+\*", "message": "Wildcard imports are discouraged"},
                {"pattern": r"(?<!def)\s+\w+\s+=\s+lambda", "message": "Consider using a function instead of assigning lambdas"}
            ],
            "javascript": [
                {"pattern": r"var\s+", "message": "Use let/const instead of var"},
                {"pattern": r"==(?!=)", "message": "Use === for comparison instead of =="},
                {"pattern": r"console\.log", "message": "Remove console.log statements in production code"}
            ]
        }
    
    def extract_code_blocks(self, text):
        """Extract code blocks from text with their language"""
        pattern = r'```(\w+)\n(.*?)\n```'
        matches = re.findall(pattern, text, re.DOTALL)
        return matches  # List of (language, code) tuples
    
    def analyze_code(self, code_text, language="python"):
        """Analyze code for potential improvements"""
        if language.lower() not in self.common_issues:
            return {"message": f"Analysis not available for {language}"}
        
        issues = []
        line_count = code_text.count('\n') + 1
        
        # Check for common issues in the code
        for issue in self.common_issues[language.lower()]:
            pattern = issue["pattern"]
            matches = re.finditer(pattern, code_text)
            for match in matches:
                # Get line number by counting newlines before the match
                line_num = code_text[:match.start()].count('\n') + 1
                issues.append({
                    "line": line_num,
                    "message": issue["message"],
                    "snippet": code_text[max(0, match.start()-10):match.end()+10]
                })
        
        # Basic code metrics
        metrics = {
            "line_count": line_count,
            "avg_line_length": sum(len(line) for line in code_text.split('\n')) / max(1, line_count),
            "comment_ratio": code_text.count('#') / max(1, line_count) if language == "python" else 0
        }
        
        # Add to analysis history
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "language": language,
            "issues": issues,
            "metrics": metrics
        }
        self.analysis_history.append(analysis)
        
        return analysis
    
    def get_improvement_suggestions(self, analysis):
        """Generate improvement suggestions based on analysis"""
        suggestions = []
        
        # Suggestions based on issues
        if analysis["issues"]:
            for i, issue in enumerate(analysis["issues"][:5]):  # Limit to top 5 issues
                suggestions.append(f"{i+1}. Line {issue['line']}: {issue['message']}")
        
        # Suggestions based on metrics
        metrics = analysis["metrics"]
        if metrics["avg_line_length"] > 80:
            suggestions.append("Consider shortening lines to improve readability (< 80 chars)")
        
        if analysis["language"] == "python" and metrics["comment_ratio"] < 0.1:
            suggestions.append("Add more comments to explain complex logic")
        
        return suggestions
    
    def get_recent_analyses(self, limit=5):
        """Get recent code analyses"""
        return self.analysis_history[-limit:] if self.analysis_history else []

# First initialize the CodeAnalyzer
code_analyzer = CodeAnalyzer()

# Then add this to your tabs[4] (Daily Logs tab)
# Add Code Analysis section
st.subheader("Code Analysis")

# Check if there are any code analyses
recent_analyses = code_analyzer.get_recent_analyses()
if recent_analyses:
    # Display recent code analyses
    for i, analysis in enumerate(recent_analyses):
        with st.expander(f"Analysis {i+1} - {analysis['language']} ({analysis['timestamp'].split('T')[0]})"):
            st.markdown(f"**Language:** {analysis['language']}")
            st.markdown(f"**Metrics:**")
            for metric, value in analysis['metrics'].items():
                st.markdown(f"- {metric.replace('_', ' ').title()}: {value:.2f}")
            
            st.markdown(f"**Issues Found:** {len(analysis['issues'])}")
            if analysis['issues']:
                for issue in analysis['issues']:
                    st.markdown(f"- **Line {issue['line']}:** {issue['message']}")
                    st.code(issue['snippet'], language=analysis['language'])
else:
    st.info("No code analyses available yet. Submit code for analysis.")

# Add a code analysis form
st.subheader("Analyze New Code")
with st.form("code_analysis_form"):
    language = st.selectbox("Language", ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go"])
    code_to_analyze = st.text_area("Paste code to analyze")
    analyze_button = st.form_submit_button("Analyze Code")

if analyze_button and code_to_analyze:
    analysis = code_analyzer.analyze_code(code_to_analyze, language.lower())
    
    st.subheader("Analysis Results")
    st.markdown(f"**Language:** {language}")
    st.markdown(f"**Metrics:**")
    for metric, value in analysis['metrics'].items():
        st.markdown(f"- {metric.replace('_', ' ').title()}: {value:.2f}")
    
    st.markdown(f"**Issues Found:** {len(analysis['issues'])}")
    if analysis['issues']:
        for issue in analysis['issues']:
            st.markdown(f"- **Line {issue['line']}:** {issue['message']}")
            st.code(issue['snippet'], language=language.lower())
    
    st.markdown("**Improvement Suggestions:**")
    suggestions = code_analyzer.get_improvement_suggestions(analysis)
    for suggestion in suggestions:
        st.markdown(f"- {suggestion}") 