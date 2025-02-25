"""
Matrix Terminal UI for TRILOGY Brain

A cyberpunk-inspired terminal interface with Matrix styling.
"""
import streamlit as st
import time
from typing import Dict, Any, List, Optional
from ui.components.terminal import TerminalComponent
from ui.components.dashboard import DashboardComponent
from ui.components.visualizations import VisualizationsComponent

class MatrixTerminal:
    """
    A Matrix-inspired terminal interface for Streamlit
    
    Features:
    - Cyberpunk-styled UI
    - Typing animations
    - Header and display components
    - Integrated terminal, dashboard, and visualization components
    """
    
    def __init__(self, initialize_now=False):
        """
        Initialize Matrix Terminal
        
        Args:
            initialize_now: Whether to initialize immediately
        """
        self.initialized = False
        self.theme_colors = {
            "primary": "#00ff41",
            "background": "#0d0d0d",
            "text": "#00ff41"
        }
        
        # Initialize components
        self.terminal = TerminalComponent(self.theme_colors)
        self.dashboard = DashboardComponent(self.theme_colors)
        self.visualizations = VisualizationsComponent(self.theme_colors)
        
        if initialize_now:
            self.initialize()
    
    def initialize(self):
        """Initialize the terminal UI"""
        if not self.initialized:
            self._setup_css()
            self.initialized = True
    
    def _setup_css(self):
        """Set up enhanced Matrix terminal CSS"""
        st.markdown("""
        <style>
        /* Matrix Terminal UI - Enhanced */
        :root {
            --neon-green: #00ff41;
            --neon-blue: #4c8dff;
            --neon-purple: #9d00ff;
            --dark-bg: #0d0d0d;
            --matrix-font: 'Courier New', monospace;
        }
        
        .matrix-terminal {
            background-color: var(--dark-bg);
            border: 1px solid var(--neon-green);
            color: var(--neon-green);
            font-family: var(--matrix-font);
            padding: 15px;
            border-radius: 4px;
            height: auto;
            max-height: 500px;
            overflow-y: auto;
            margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
        }
        
        .matrix-line {
            line-height: 1.5;
            margin-bottom: 8px;
            white-space: pre-wrap;
            word-break: break-word;
        }
        
        .matrix-user-line {
            color: var(--neon-blue);
            border-left: 2px solid var(--neon-blue);
            padding-left: 10px;
        }
        
        .matrix-system-line {
            color: var(--neon-green);
            border-left: 2px solid var(--neon-green);
            padding-left: 10px;
        }
        
        .matrix-header {
            text-align: center;
            font-family: var(--matrix-font);
            color: var(--neon-green);
            margin-bottom: 30px;
            text-shadow: 0 0 8px var(--neon-green);
            background-color: rgba(13, 13, 13, 0.95);
            padding: 20px;
            border-radius: 5px;
            border: 1px solid rgba(0, 255, 65, 0.3);
        }
        
        .matrix-title {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
            letter-spacing: 3px;
        }
        
        .matrix-subtitle {
            font-size: 16px;
            opacity: 0.8;
            margin-bottom: 15px;
        }
        
        .matrix-branding {
            margin-top: 15px;
            font-size: 14px;
        }
        
        .matrix-branding-link {
            color: var(--neon-purple);
            text-decoration: none;
            transition: all 0.3s ease;
            border: 1px solid var(--neon-purple);
            padding: 5px 10px;
            border-radius: 3px;
        }
        
        .matrix-branding-link:hover {
            background-color: rgba(157, 0, 255, 0.2);
            text-shadow: 0 0 5px var(--neon-purple);
            box-shadow: 0 0 10px rgba(157, 0, 255, 0.5);
        }
        
        /* Grid background effect */
        .matrix-container {
            position: relative;
        }
        
        .matrix-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
            background-size: 20px 20px;
            z-index: -1;
            opacity: 0.2;
            pointer-events: none;
        }
        
        /* Pulse animation for terminals */
        @keyframes matrix-pulse {
            0% { box-shadow: 0 0 15px rgba(0, 255, 65, 0.3); }
            50% { box-shadow: 0 0 25px rgba(0, 255, 65, 0.5); }
            100% { box-shadow: 0 0 15px rgba(0, 255, 65, 0.3); }
        }
        
        .matrix-terminal {
            animation: matrix-pulse 4s infinite;
        }
        
        /* Typing effect */
        .typing-effect {
            display: inline-block;
            overflow: hidden;
            white-space: nowrap;
            border-right: 2px solid var(--neon-green);
            animation: typing 3.5s steps(30, end), blink-caret 0.75s step-end infinite;
        }
        
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: var(--neon-green) }
        }
        
        /* Button styles */
        .matrix-button {
            background-color: rgba(0, 255, 65, 0.1);
            color: var(--neon-green);
            border: 1px solid var(--neon-green);
            border-radius: 3px;
            padding: 5px 10px;
            font-family: var(--matrix-font);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .matrix-button:hover {
            background-color: rgba(0, 255, 65, 0.2);
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        }
        
        /* Make Streamlit UI elements match the theme */
        .stTextInput > div > div {
            background-color: rgba(0, 0, 0, 0.5) !important;
            border-color: var(--neon-green) !important;
            color: var(--neon-green) !important;
        }
        
        .stTextInput input {
            color: var(--neon-green) !important;
            font-family: var(--matrix-font) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def display_header(self, title="TRILOGY BRAIN", subtitle="Advanced AI Orchestration System"):
        """
        Display the Matrix header
        
        Args:
            title: Main title text
            subtitle: Subtitle text
        """
        st.markdown(f"""
        <div class="matrix-header">
            <div class="matrix-title">{title}</div>
            <div class="matrix-subtitle">{subtitle}</div>
            <div class="matrix-branding">
                <a href="https://villageofthousands.io" target="_blank" class="matrix-branding-link">
                    Powered by VillageOfThousands.io
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def display_terminal(self, lines: List[Dict[str, str]], animate: bool = False, max_lines: int = 20):
        """
        Display a Matrix terminal with lines
        
        Args:
            lines: List of dictionaries with 'role' and 'text'
            animate: Whether to animate the last line
            max_lines: Maximum number of lines to display
        """
        st.markdown('<div class="matrix-terminal">', unsafe_allow_html=True)
        
        # Limit the number of lines
        display_lines = lines[-max_lines:] if len(lines) > max_lines else lines
        
        # Display all but last line normally
        for i, line in enumerate(display_lines[:-1] if display_lines else []):
            line_class = "matrix-user-line" if line.get("role") == "user" else "matrix-system-line"
            st.markdown(f'<div class="matrix-line {line_class}">{line.get("text", "")}</div>', unsafe_allow_html=True)
        
        # Display last line with typing animation if requested
        if display_lines:
            last_line = display_lines[-1]
            line_class = "matrix-user-line" if last_line.get("role") == "user" else "matrix-system-line"
            
            if animate:
                st.markdown(f'<div class="matrix-line {line_class} typing-effect">{last_line.get("text", "")}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="matrix-line {line_class}">{last_line.get("text", "")}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def display_typing_text(self, text: str, speed: float = 0.03, container=None):
        """
        Display text with a typing effect
        
        Args:
            text: Text to display
            speed: Typing speed (seconds per character)
            container: Optional container to place the text in
        """
        # Create a placeholder
        if container:
            placeholder = container.empty()
        else:
            placeholder = st.empty()
        
        for i in range(len(text) + 1):
            # Display text up to index i
            partial_text = text[:i]
            placeholder.markdown(f'<div class="matrix-system-line">{partial_text}</div>', unsafe_allow_html=True)
            
            # Wait for the typing effect
            time.sleep(speed)
    
    def set_theme(self, theme_colors: Dict[str, str]):
        """
        Set the color theme for the Matrix terminal
        
        Args:
            theme_colors: Dictionary with primary, background, and text colors
        """
        self.theme_colors = theme_colors
        
        # Update components with new theme
        self.terminal = TerminalComponent(theme_colors)
        self.dashboard = DashboardComponent(theme_colors)
        self.visualizations = VisualizationsComponent(theme_colors)
        
        # Update CSS variables
        st.markdown(f"""
        <style>
        :root {{
            --neon-green: {theme_colors['primary']};
            --dark-bg: {theme_colors['background']};
            --text-color: {theme_colors['text']};
            --matrix-font: 'Courier New', monospace;
        }}
        </style>
        """, unsafe_allow_html=True) 