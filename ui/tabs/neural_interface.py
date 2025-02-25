"""
Neural Interface Tab for TRILOGY Brain
"""
import streamlit as st
from typing import Dict, Any, List, Optional
import time

def render_neural_interface(trilogy_brain, session_state):
    """
    Render the Neural Interface tab
    
    Args:
        trilogy_brain: TrilogyBrain instance
        session_state: Streamlit session state
    """
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display reasoning steps if available
            if message["role"] == "assistant" and "thinking" in message and message["thinking"]:
                with st.expander("View Reasoning Process", expanded=False):
                    st.markdown(message["thinking"])
                    
                    # Add visual flow diagram for reasoning steps if available
                    if "reasoning_steps" in message and len(message["reasoning_steps"]) > 1:
                        render_reasoning_flow(message["reasoning_steps"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input for new query
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message
        session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Process with TRILOGY Brain
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🧠 Thinking...")
            
            # Process the query with CoT context
            context = {
                "thinking_depth": session_state.thinking_depth,
                "model_override": session_state.model_override if session_state.model_override != "auto" else None,
                "use_cot": session_state.get("use_cot", True)
            }
            
            # Check if research mode is enabled
            if session_state.get("research_mode", False):
                result = trilogy_brain.research_with_cot(prompt, context=context, thinking_depth=session_state.thinking_depth)
            else:
                result = trilogy_brain.process_query(prompt, context)
            
            # Display response
            message_placeholder.markdown(result["answer"])
            
            # Add to session state
            session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
                "thinking": result.get("thinking", ""),
                "reasoning_steps": result.get("reasoning_steps", []),
                "metadata": {
                    "model": result.get("model", "unknown"),
                    "execution_time": result.get("metadata", {}).get("execution_time", 0)
                }
            })

def render_reasoning_flow(reasoning_steps):
    """
    Render reasoning flow diagram
    
    Args:
        reasoning_steps: List of reasoning steps
    """
    steps_html = """
    <div class="reasoning-flow">
    """
    
    for i, step in enumerate(reasoning_steps):
        # Get step content - handle both string and dictionary formats
        step_content = step
        if isinstance(step, dict) and "content" in step:
            step_content = step["content"]
            
        # Truncate long content
        step_summary = step_content[:100] + '...' if len(step_content) > 100 else step_content
        
        steps_html += f"""
        <div class="reasoning-step">
            <div class="step-number">{i+1}</div>
            <div class="step-content">{step_summary}</div>
        </div>
        """
        
        if i < len(reasoning_steps) - 1:
            steps_html += '<div class="step-arrow">→</div>'
            
    steps_html += "</div>"
    
    st.markdown(steps_html, unsafe_allow_html=True) 