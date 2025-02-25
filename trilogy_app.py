"""
TRILOGY Brain Main Application

Entry point for the TRILOGY Brain system with Streamlit UI.
"""
import streamlit as st
import os
import time
import logging
import sys
from datetime import datetime
import pandas as pd
import json
import base64

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("trilogy")

# Log startup info
logger.info("Starting TRILOGY Brain application...")

# Import core components
from core.trilogy_brain import TrilogyBrain
from models.registry import ModelRegistry
from core.router import Router
try:
    from core.vector_memory import VectorMemorySystem, VECTOR_MEMORY_AVAILABLE
except ImportError:
    VECTOR_MEMORY_AVAILABLE = False
    logger.warning("Vector memory system not available - some advanced features will be disabled")
from utils.telemetry import Telemetry
from ui.matrix_terminal import MatrixTerminal
from utils.analytics import ModelAnalytics
from core.resilience import CircuitBreaker
from core.self_improvement.learner import PerformanceLearner
from core.self_improvement.preference_learner import UserPreferenceLearner
from ui.components.docs_viewer import DocsViewer
from ui.adaptive_interface import AdaptiveInterface

# Add import check for plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger.warning("Plotly not available - analytics features will be disabled")

# Set page config - must be the first Streamlit command
st.set_page_config(
    page_title="TRILOGY Brain",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Log successful initialization
logger.info("Page configuration initialized")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "thinking_depth" not in st.session_state:
    st.session_state.thinking_depth = 0.7
    
if "model_override" not in st.session_state:
    st.session_state.model_override = "auto"

# Initialize the TRILOGY Brain ecosystem
@st.cache_resource
def initialize_trilogy_brain():
    """Initialize and cache the TRILOGY Brain system"""
    # Initialize components
    model_registry = ModelRegistry()
    router = Router()
    
    # Initialize memory system with proper fallback
    if VECTOR_MEMORY_AVAILABLE:
        try:
            memory_system = VectorMemorySystem()
            logger.info("Using Vector Memory System")
        except Exception as e:
            # Fallback to basic memory system
            from core.memory_system import MemorySystem
            memory_system = MemorySystem()
            logger.warning(f"Vector Memory System initialization failed, using basic Memory System: {e}")
    else:
        from core.memory_system import MemorySystem
        memory_system = MemorySystem()
        logger.warning("Using basic Memory System (vector memory not available)")
    
    telemetry = Telemetry()
    
    # Register available models including Ollama
    from models.ollama import OllamaModel
    ollama_model = OllamaModel()
    
    # Register models with the registry
    if ollama_model.is_available():
        available_models = ollama_model.list_models()
        for model_name in available_models:
            model_registry.register_model(
                name=f"ollama_{model_name}",
                model_type="ollama",
                config={"default_model": model_name},
                initializer=lambda config: OllamaModel(**config)
            )
        logger.info(f"Registered {len(available_models)} Ollama models")
    
    # Initialize Claude models if available
    try:
        from models.claude import ClaudeModel
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            for model_name in ["claude-3-opus-20240229", "claude-3-sonnet-20240229"]:
                model_registry.register_model(
                    name=model_name,
                    model_type="claude",
                    config={"api_key": api_key, "model": model_name},
                    initializer=lambda config: ClaudeModel(**config)
                )
            logger.info("Registered Claude models")
    except Exception as e:
        logger.warning(f"Claude API not available: {e}")
    
    # Initialize DeepSeek models if available
    try:
        from models.deepseek import DeepSeekModel
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if api_key:
            model_registry.register_model(
                name="deepseek-coder",
                model_type="deepseek",
                config={"api_key": api_key, "model": "deepseek-coder"},
                initializer=lambda config: DeepSeekModel(**config)
            )
            logger.info("Registered DeepSeek models")
    except Exception as e:
        logger.warning(f"DeepSeek API not available: {e}")
    
    # Initialize Perplexity models if available
    try:
        from models.perplexity import PerplexityModel
        api_key = os.environ.get("PERPLEXITY_API_KEY")
        if api_key:
            for model_name in ["sonar-medium-online", "sonar-small-online"]:
                model_registry.register_model(
                    name=model_name,
                    model_type="perplexity",
                    config={"api_key": api_key, "model": model_name},
                    initializer=lambda config: PerplexityModel(**config)
                )
            logger.info("Registered Perplexity models")
    except Exception as e:
        logger.warning(f"Perplexity API not available: {e}")
    
    # Initialize analytics
    analytics = ModelAnalytics()
    
    # Initialize TRILOGY Brain with analytics
    trilogy_brain = TrilogyBrain(
        model_registry=model_registry,
        router=router,
        memory_system=memory_system,
        telemetry=telemetry,
        analytics=analytics  # Add analytics parameter
    )
    
    return trilogy_brain

# Initialize the system
trilogy_brain = initialize_trilogy_brain()
matrix_terminal = MatrixTerminal(initialize_now=True)

# Initialize the new components
performance_learner = PerformanceLearner()
preference_learner = UserPreferenceLearner()
adaptive_interface = AdaptiveInterface()

# Theme selector in sidebar
with st.sidebar:
    st.title("TRILOGY Brain")
    theme = st.selectbox(
        "Theme",
        options=["Matrix (Default)", "Cyberpunk Blue", "Retro Amber", "Light"],
        index=0,
        key="theme_selector"
    )
    
    # Apply theme
    if theme == "Matrix (Default)":
        theme_colors = {
            "primary": "#00ff41",
            "background": "#0d0d0d",
            "text": "#00ff41"
        }
    elif theme == "Cyberpunk Blue":
        theme_colors = {
            "primary": "#00ffff",
            "background": "#0a001a",
            "text": "#00ffff"
        }
    elif theme == "Retro Amber":
        theme_colors = {
            "primary": "#ffb000",
            "background": "#100800",
            "text": "#ffb000"
        }
    else:  # Light
        theme_colors = {
            "primary": "#1e88e5",
            "background": "#ffffff",
            "text": "#212121"
        }
        
    # Update MatrixTerminal colors
    matrix_terminal.set_theme(theme_colors)
    
    # Show system info
    st.caption(f"Connected to {len(trilogy_brain.model_registry.list_available_models())} models")
    st.caption("Powered by [VillageOfThousands.io](https://villageofthousands.io)")

# Display Matrix header
matrix_terminal.display_header()

# Main app
st.title("🧠 TRILOGY Brain Dashboard")
st.markdown("Advanced AI orchestration system with local Ollama integration")

# Create tabs
tabs = st.tabs(["Neural Interface", "System Dashboard", "Memory Explorer", "Analytics", "Plugins", "Documentation", "Settings"])

# Neural Interface tab
with tabs[0]:
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display reasoning steps if available
            if message["role"] == "assistant" and "thinking" in message and message["thinking"]:
                with st.expander("View Reasoning Process", expanded=False):
                    st.markdown(message["thinking"])
                    
                    # Add visual flow diagram for reasoning steps if available
                    if "reasoning_steps" in message and len(message["reasoning_steps"]) > 1:
                        steps_html = """
                        <div class="reasoning-flow">
                        """
                        
                        for i, step in enumerate(message["reasoning_steps"]):
                            steps_html += f"""
                            <div class="reasoning-step">
                                <div class="step-number">{i+1}</div>
                                <div class="step-content">{step[:100] + '...' if len(step) > 100 else step}</div>
                            </div>
                            """
                            if i < len(message["reasoning_steps"]) - 1:
                                steps_html += '<div class="step-arrow">→</div>'
                                
                        steps_html += "</div>"
                        
                        st.markdown(steps_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input for new query
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Process with TRILOGY Brain
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🧠 Thinking...")
            
            # Process the query with CoT context
            context = {
                "thinking_depth": st.session_state.thinking_depth,
                "model_override": st.session_state.model_override if st.session_state.model_override != "auto" else None,
                "use_cot": st.session_state.get("use_cot", True)  # Add CoT flag
            }
            
            start_time = time.time()
            try:
                # Record query for learning
                model_recommendation = performance_learner.recommend_model(prompt)
                
                # Use circuit breaker for model invocation
                circuit = CircuitBreaker(f"model_{model_recommendation}")
                result = circuit.execute(
                    trilogy_brain.process_query, 
                    prompt, 
                    context={"model_override": model_recommendation}
                )
                
                execution_time = time.time() - start_time
                # Record performance for learning
                performance_learner.record_performance(
                    query=prompt,
                    model_used=result.get("model", model_recommendation),
                    execution_time=execution_time,
                    success=True
                )
                
                # Track user interaction
                adaptive_interface.track_interaction("query_submission", "success")
                
                # Display response
                message_placeholder.markdown(result["answer"])
                
                # Add to session state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "thinking": result.get("thinking", ""),
                    "reasoning_steps": result.get("reasoning_steps", []),
                    "metadata": {
                        "model": result.get("model", "unknown"),
                        "execution_time": result.get("metadata", {}).get("execution_time", 0)
                    }
                })
            except Exception as e:
                execution_time = time.time() - start_time
                # Record failure
                performance_learner.record_performance(
                    query=prompt,
                    model_used=model_recommendation,
                    execution_time=execution_time,
                    success=False
                )
                # Track error
                adaptive_interface.track_interaction("query_submission", "error")
                st.error(f"Error processing query: {str(e)}")

# System Dashboard tab
with tabs[1]:
    st.header("System Status")
    
    # System metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Models", len(trilogy_brain.model_registry.list_available_models()))
    
    with col2:
        # Calculate average response time
        assistant_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]
        avg_time = sum([m.get("metadata", {}).get("execution_time", 0) for m in assistant_msgs]) / max(1, len(assistant_msgs))
        st.metric("Avg Response Time", f"{avg_time:.2f}s")
    
    with col3:
        st.metric("Messages", len(st.session_state.messages))
    
    # Model availability
    st.subheader("Available Models")
    models = trilogy_brain.model_registry.list_available_models()
    
    if models:
        model_data = []
        for model_name in models:
            model_info = trilogy_brain.model_registry.get_model_info(model_name)
            model_data.append({
                "Model": model_name,
                "Type": model_info["type"],
                "Status": "Available"
            })
        
        st.table(pd.DataFrame(model_data))
    else:
        st.warning("No models available. Please check your configuration.")
    
    # System activity
    st.subheader("Recent Activity")
    activity = trilogy_brain.telemetry.get_recent_activity(10)
    
    if activity:
        st.table(pd.DataFrame(activity))
    else:
        st.info("No activity recorded yet.")

# Memory Explorer tab
with tabs[2]:
    st.header("Memory Explorer")
    
    if not VECTOR_MEMORY_AVAILABLE:
        st.warning("""
        Advanced memory features are not available. To enable vector-based memory:
        1. Install required packages: `pip install chromadb sentence-transformers`
        2. Restart the application
        """)
    
    try:
        # Search and filter
        search_col, filter_col = st.columns([3, 1])
        
        with search_col:
            search_query = st.text_input("Search Memories", placeholder="Enter search text...")
        
        with filter_col:
            memory_type = st.selectbox(
                "Memory Type",
                options=["All", "Conversation", "Document", "Code"],
                index=0
            )
        
        # Get memory visualization data
        if hasattr(trilogy_brain.memory_system, 'visualize_memory_graph'):
            graph_data = trilogy_brain.memory_system.visualize_memory_graph(limit=50)
            
            if graph_data["nodes"]:
                st.subheader("Memory Graph")
                
                # Create a force-directed graph with D3.js
                st.markdown("""
                <div id="memory-graph" style="width:100%; height:400px; border:1px solid #ddd; border-radius:5px;"></div>
                <script src="https://d3js.org/d3.v7.min.js"></script>
                <script>
                // Memory graph data
                const graph = %s;
                
                // Create D3 force simulation
                const width = document.getElementById('memory-graph').clientWidth;
                const height = 400;
                
                const svg = d3.select("#memory-graph")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height);
                    
                // Create force simulation
                const simulation = d3.forceSimulation(graph.nodes)
                    .force("link", d3.forceLink(graph.links).id(d => d.id))
                    .force("charge", d3.forceManyBody().strength(-150))
                    .force("center", d3.forceCenter(width / 2, height / 2));
                
                // Draw links
                const link = svg.append("g")
                    .selectAll("line")
                    .data(graph.links)
                    .enter().append("line")
                    .attr("stroke", "#999")
                    .attr("stroke-opacity", 0.6)
                    .attr("stroke-width", d => Math.sqrt(d.value));
                
                // Draw nodes
                const color = d3.scaleOrdinal(d3.schemeCategory10);
                
                const node = svg.append("g")
                    .selectAll("circle")
                    .data(graph.nodes)
                    .enter().append("circle")
                    .attr("r", 5)
                    .attr("fill", d => color(d.group))
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));
                
                // Add tooltips
                node.append("title")
                    .text(d => d.full_query);
                
                // Update positions
                simulation.on("tick", () => {
                    link
                        .attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);
                    
                    node
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);
                });
                
                // Drag functions
                function dragstarted(event, d) {
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }
                
                function dragged(event, d) {
                    d.fx = event.x;
                    d.fy = event.y;
                }
                
                function dragended(event, d) {
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }
                </script>
                """ % json.dumps(graph_data), unsafe_allow_html=True)
            else:
                st.info("No memory data available for visualization yet.")
        else:
            st.info("Memory visualization not available with basic memory system")
        
        # Memory search results
        st.subheader("Memory Search")
        
        # Perform search if query or filter is provided
        if search_query or memory_type != "All":
            filters = None
            if memory_type != "All":
                filters = {"type": memory_type.lower()}
            
            # Search memories
            if hasattr(trilogy_brain.memory_system, 'search_memories'):
                memories = trilogy_brain.memory_system.search_memories(
                    search_text=search_query or "",
                    filters=filters
                )
                
                if memories:
                    for memory in memories:
                        with st.expander(f"{memory['query'][:50]}... ({memory['metadata'].get('timestamp', 'Unknown date')})"):
                            st.markdown(f"**Query:** {memory['query']}")
                            st.markdown(f"**Response:** {memory['response']}")
                            
                            # Add metadata display
                            st.markdown("**Metadata:**")
                            st.json(memory['metadata'])
                            
                            # Add delete button
                            if st.button(f"Delete Memory {memory['id'][:8]}...", key=f"delete_{memory['id']}"):
                                if trilogy_brain.memory_system.delete_memory(memory['id']):
                                    st.success("Memory deleted")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete memory")
                else:
                    st.info("No memories found matching your criteria")
        else:
            # Show memory stats
            stats = trilogy_brain.memory_system.get_memory_stats()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Memories", stats.get("count", 0))
            
            with col2:
                if stats.get("newest"):
                    newest = datetime.fromisoformat(stats["newest"])
                    st.metric("Newest Memory", newest.strftime("%Y-%m-%d"))
                    
            with col3:
                if stats.get("oldest"):
                    oldest = datetime.fromisoformat(stats["oldest"])
                    st.metric("Oldest Memory", oldest.strftime("%Y-%m-%d"))
            
            # Show recent memories
            st.subheader("Recent Memories")
            
            if hasattr(trilogy_brain.memory_system, 'search_memories'):
                recent_memories = trilogy_brain.memory_system.search_memories(
                    search_text="",
                    limit=5
                )
                
                if recent_memories:
                    for memory in recent_memories:
                        with st.expander(f"{memory['query'][:50]}... ({memory['metadata'].get('timestamp', 'Unknown date')})"):
                            st.markdown(f"**Query:** {memory['query']}")
                            st.markdown(f"**Response:** {memory['response']}")
                else:
                    st.info("No memories found in the system")
    except Exception as e:
        st.error(f"Error in Memory Explorer: {e}")
        st.info("Try refreshing the model registry or check system logs for details")

# Analytics tab
with tabs[3]:
    st.header("Model Analytics")
    
    if not PLOTLY_AVAILABLE:
        st.warning("""
        Analytics features are not available. To enable analytics:
        1. Install required packages: `pip install plotly`
        2. Restart the application
        """)
        st.stop()
    
    # Time period selection
    time_period = st.selectbox(
        "Time Period",
        options=["Last 7 days", "Last 30 days", "Last 90 days"],
        index=0,
        key="analytics_time_period"
    )
    
    days = 7
    if time_period == "Last 30 days":
        days = 30
    elif time_period == "Last 90 days":
        days = 90
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    try:
        # Get performance chart data
        chart_data = trilogy_brain.analytics.create_performance_chart(days=days)
        
        with col1:
            st.subheader("Response Time by Model")
            st.plotly_chart(
                chart_data["fig_performance"], 
                use_container_width=True,
                key="performance_chart"
            )
        
        with col2:
            st.subheader("Domain Effectiveness")
            st.plotly_chart(
                chart_data["fig_domains"], 
                use_container_width=True,
                key="domains_chart"
            )
        
        # Usage trends
        st.subheader("Usage Trends")
        trends_data = trilogy_brain.analytics.get_usage_trends(days=days)
        st.plotly_chart(
            trends_data["fig"], 
            use_container_width=True,
            key="trends_chart"
        )
        
        # Raw performance data
        st.subheader("Performance Data")
        perf_data = pd.DataFrame(chart_data["data"]["performance_data"])
        if not perf_data.empty:
            st.dataframe(perf_data, key="performance_dataframe")
        else:
            st.info("No performance data available yet.")
    except Exception as e:
        st.error(f"Error generating analytics charts: {e}")
        st.info("This could happen if you haven't processed any queries yet.")

# Plugins tab
with tabs[4]:
    st.header("Plugins")
    
    try:
        # Get plugin list
        plugins = trilogy_brain.list_plugins()
        
        # Display active plugins
        st.subheader("Active Plugins")
        
        if plugins["active"]:
            for plugin in plugins["active"]:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    with st.expander(f"{plugin['name']} v{plugin['version']}"):
                        st.markdown(f"**Description:** {plugin['description']}")
                        st.markdown(f"**Type:** {plugin['type']}")
                        st.markdown(f"**Capabilities:** {', '.join(plugin['capabilities'])}")
                        
                        # For tool plugins, show available tools
                        if plugin['type'] == 'tool':
                            tools = [tool for tool in trilogy_brain.get_available_tools() if tool['plugin'] == plugin['name']]
                            if tools:
                                st.markdown("#### Available Tools")
                                for tool in tools:
                                    st.markdown(f"- **{tool['name']}**: {tool['description']}")
                
                with col2:
                    if st.button(f"Deactivate {plugin['name']}", key=f"deactivate_{plugin['name']}"):
                        if trilogy_brain.plugin_manager.deactivate_plugin(plugin['name']):
                            st.success(f"Deactivated {plugin['name']}")
                            st.rerun()
                        else:
                            st.error(f"Failed to deactivate {plugin['name']}")
        else:
            st.info("No active plugins")
        
        # Display registered plugins
        st.subheader("Available Plugins")
        
        if plugins["registered"]:
            for plugin in plugins["registered"]:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{plugin['name']}** v{plugin['version']} - {plugin['description']}")
                
                with col2:
                    if st.button(f"Activate {plugin['name']}", key=f"activate_{plugin['name']}"):
                        if trilogy_brain.plugin_manager.activate_plugin(plugin['name']):
                            st.success(f"Activated {plugin['name']}")
                            st.rerun()
                        else:
                            st.error(f"Failed to activate {plugin['name']}")
        else:
            st.info("No additional plugins available")
        
        # Plugin testing section
        st.subheader("Plugin Testing")
        
        # Only show if there are active plugins
        if plugins["active"]:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_plugin = st.selectbox(
                    "Select Plugin",
                    options=[plugin["name"] for plugin in plugins["active"]]
                )
            
            with col2:
                # Get commands for the selected plugin
                if selected_plugin:
                    plugin_type = next((p["type"] for p in plugins["active"] if p["name"] == selected_plugin), None)
                    
                    if plugin_type == "tool":
                        tools = [tool for tool in trilogy_brain.get_available_tools() if tool["plugin"] == selected_plugin]
                        commands = [tool["command"] for tool in tools]
                    else:
                        # Default commands
                        commands = ["execute"]
                    
                    selected_command = st.selectbox(
                        "Command",
                        options=commands
                    )
            
            # Parameters for the command
            st.subheader("Parameters")
            
            params = {}
            
            # Add text parameter
            if plugin_type == "tool" and selected_command in ["calculate", "solve"]:
                if selected_command == "calculate":
                    expression = st.text_input("Expression", "2 + 2 * 3")
                    params["expression"] = expression
                elif selected_command == "solve":
                    equation = st.text_input("Equation", "x+5=10")
                    params["equation"] = equation
            else:
                text = st.text_area("Text", "Hello world")
                params["text"] = text
            
            # Execute button
            if st.button("Execute Plugin"):
                with st.spinner("Executing plugin..."):
                    result = trilogy_brain.execute_plugin(selected_plugin, selected_command, **params)
                    
                    st.subheader("Result")
                    st.json(result)
        else:
            st.info("Activate plugins to test them")

    except Exception as e:
        st.error(f"Error loading plugins: {e}")
        st.info("Make sure the plugin system is properly initialized")

# Documentation tab
with tabs[5]:
    docs_viewer = DocsViewer()
    docs_viewer.render()

# Settings tab
with tabs[6]:
    st.header("System Settings")
    
    # Add chain of thought toggle
    use_cot = st.toggle(
        "Enable Chain of Thought Reasoning",
        value=True,
        help="When enabled, the system will break down complex problems into step-by-step reasoning"
    )
    
    # Update session state
    st.session_state.use_cot = use_cot
    
    # Thinking depth slider
    st.session_state.thinking_depth = st.slider(
        "Thinking Depth",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.thinking_depth,
        step=0.1,
        help="Controls how detailed the AI's reasoning process will be"
    )
    
    # Model selection
    available_models = ["auto"] + trilogy_brain.model_registry.list_available_models()
    st.session_state.model_override = st.selectbox(
        "Default Model",
        options=available_models,
        index=available_models.index(st.session_state.model_override) if st.session_state.model_override in available_models else 0,
        help="Select which model to use by default"
    )
    
    # System actions
    st.subheader("Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear Conversation History"):
            st.session_state.messages = []
            st.success("Conversation history cleared!")
            st.rerun()
    
    with col2:
        if st.button("Refresh Model Registry"):
            # Re-initialize to refresh models
            st.cache_resource.clear()
            trilogy_brain = initialize_trilogy_brain()
            st.success("Model registry refreshed!")
            st.rerun()

    # After other settings
    st.subheader("Conversation Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Conversation"):
            # Create exportable JSON
            conversation_data = {
                "messages": st.session_state.messages,
                "timestamp": datetime.now().isoformat()
            }
            
            # Convert to downloadable format
            json_str = json.dumps(conversation_data, indent=2)
            b64 = base64.b64encode(json_str.encode()).decode()
            href = f'<a href="data:file/json;base64,{b64}" download="trilogy_conversation.json">Download Conversation</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with col2:
        uploaded_file = st.file_uploader("Import Conversation", type="json")
        if uploaded_file is not None:
            try:
                conversation_data = json.load(uploaded_file)
                if "messages" in conversation_data:
                    st.session_state.messages = conversation_data["messages"]
                    st.success("Conversation imported successfully!")
                    st.rerun()
                else:
                    st.error("Invalid conversation file format")
            except Exception as e:
                st.error(f"Error importing conversation: {e}")

# Add CSS for reasoning visualization
st.markdown("""
<style>
.reasoning-flow {
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    overflow-x: auto;
    padding: 10px 0;
    margin: 10px 0;
}

.reasoning-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 120px;
    max-width: 200px;
    background-color: rgba(0, 255, 65, 0.1);
    border: 1px solid rgba(0, 255, 65, 0.3);
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
}

.step-number {
    font-weight: bold;
    font-size: 16px;
    color: #00ff41;
    margin-bottom: 5px;
}

.step-content {
    font-size: 12px;
    text-align: center;
}

.step-arrow {
    color: #00ff41;
    font-size: 24px;
    margin: 0 5px;
}
</style>
""", unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    logger.info("TRILOGY Brain application started") 