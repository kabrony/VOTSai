"""
Terminal UI Component for TRILOGY Brain

Provides a terminal-style interface for interacting with the AI system.
"""
import streamlit as st
from typing import Dict, Any, List, Optional

class TerminalComponent:
    """
    Terminal UI component for a command-line style interface
    
    Features:
    - Terminal-style appearance with scan lines and retro effects
    - Command input and history
    - Styled output
    """
    
    def __init__(self, 
                theme_colors: Optional[Dict[str, str]] = None,
                terminal_id: str = "main"):
        """
        Initialize the terminal component
        
        Args:
            theme_colors: Dictionary with primary, background, and text colors
            terminal_id: Unique ID for this terminal instance
        """
        self.theme_colors = theme_colors or {
            "primary": "#00ff41",
            "background": "#0d0d0d",
            "text": "#00ff41"
        }
        self.terminal_id = terminal_id
        self.command_history = []
        self._setup_css()
        
    def _setup_css(self):
        """Initialize terminal CSS"""
        st.markdown(f"""
        <style>
        .terminal-{self.terminal_id} {{
            background-color: {self.theme_colors["background"]};
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 6px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            color: {self.theme_colors["text"]};
            position: relative;
            margin-bottom: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.4);
            overflow: hidden;
        }}
        
        .terminal-header-{self.terminal_id} {{
            border-bottom: 1px solid {self.theme_colors["primary"]};
            padding-bottom: 8px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
        }}
        
        .terminal-title-{self.terminal_id} {{
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .terminal-controls-{self.terminal_id} {{
            display: flex;
        }}
        
        .terminal-button-{self.terminal_id} {{
            height: 12px;
            width: 12px;
            border-radius: 50%;
            margin-left: 6px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .terminal-button-close-{self.terminal_id} {{
            background-color: #ff5f56;
        }}
        
        .terminal-button-minimize-{self.terminal_id} {{
            background-color: #ffbd2e;
        }}
        
        .terminal-button-maximize-{self.terminal_id} {{
            background-color: #27c93f;
        }}
        
        .terminal-content-{self.terminal_id} {{
            min-height: 200px;
            position: relative;
            padding: 8px;
        }}
        
        .terminal-prompt-{self.terminal_id}::before {{
            content: "trilogy@brain:~$ ";
            color: {self.theme_colors["primary"]};
            font-weight: bold;
        }}
        
        .terminal-cursor-{self.terminal_id} {{
            display: inline-block;
            width: 8px;
            height: 15px;
            background-color: {self.theme_colors["primary"]};
            margin-left: 4px;
            animation: blink-{self.terminal_id} 1s infinite;
            vertical-align: middle;
        }}
        
        @keyframes blink-{self.terminal_id} {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}
        
        /* Scan line effect */
        .terminal-{self.terminal_id}::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                transparent 0%,
                rgba(32, 128, 32, 0.2) 2%,
                transparent 3%,
                transparent 30%,
                rgba(32, 128, 32, 0.2) 31%,
                transparent 33%,
                transparent 60%,
                rgba(32, 128, 32, 0.2) 61%,
                transparent 63%,
                transparent 100%
            );
            background-size: 100% 100px;
            animation: scanline-{self.terminal_id} 10s linear infinite;
            pointer-events: none;
            opacity: 0.2;
            z-index: 1;
        }}
        
        @keyframes scanline-{self.terminal_id} {{
            0% {{ background-position: 0 0; }}
            100% {{ background-position: 0 100%; }}
        }}
        
        .user-command-{self.terminal_id} {{
            margin-bottom: 10px;
        }}
        
        .system-response-{self.terminal_id} {{
            color: {self.theme_colors["text"]};
            margin-bottom: 15px;
            padding-left: 20px;
            border-left: 2px solid {self.theme_colors["primary"]};
        }}
        </style>
        """, unsafe_allow_html=True)
        
    def render_terminal(self, title: str = "TRILOGY Terminal"):
        """
        Render the terminal container
        
        Args:
            title: Title for the terminal window
            
        Returns:
            Terminal content container
        """
        # Terminal container
        st.markdown(f"""
        <div class="terminal-{self.terminal_id}">
            <div class="terminal-header-{self.terminal_id}">
                <div class="terminal-title-{self.terminal_id}">{title}</div>
                <div class="terminal-controls-{self.terminal_id}">
                    <div class="terminal-button-{self.terminal_id} terminal-button-minimize-{self.terminal_id}"></div>
                    <div class="terminal-button-{self.terminal_id} terminal-button-maximize-{self.terminal_id}"></div>
                    <div class="terminal-button-{self.terminal_id} terminal-button-close-{self.terminal_id}"></div>
                </div>
            </div>
            <div class="terminal-content-{self.terminal_id}" id="terminal-content-{self.terminal_id}">
                <!-- Terminal content goes here -->
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Return a container for the terminal content
        return st.container()
    
    def command_input(self, 
                    placeholder: str = "Enter command...", 
                    key: Optional[str] = None) -> str:
        """
        Render a command input field
        
        Args:
            placeholder: Placeholder text
            key: Streamlit element key
            
        Returns:
            Entered command
        """
        input_key = key or f"terminal_command_{self.terminal_id}"
        
        # Add terminal prompt styling
        st.markdown(f'<div class="terminal-prompt-{self.terminal_id}"></div>', unsafe_allow_html=True)
        
        # Command input
        command = st.text_input(
            label="",
            placeholder=placeholder,
            key=input_key,
            label_visibility="collapsed"
        )
        
        # Add to history if a command was entered
        if command and command not in self.command_history:
            self.command_history.append(command)
            
        return command
    
    def render_output(self, 
                     content: str, 
                     is_user: bool = False,
                     add_to_container: Optional[Any] = None):
        """
        Render terminal output
        
        Args:
            content: Text content to display
            is_user: Whether this is user input (vs system output)
            add_to_container: Optional container to add the output to
        """
        # Create the HTML for the output
        class_name = f"user-command-{self.terminal_id}" if is_user else f"system-response-{self.terminal_id}"
        
        if is_user:
            html = f"""
            <div class="{class_name}">
                <span class="terminal-prompt-{self.terminal_id}"></span>
                {content}
            </div>
            """
        else:
            html = f'<div class="{class_name}">{content}</div>'
        
        # Render in the appropriate container
        if add_to_container:
            add_to_container.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown(html, unsafe_allow_html=True)
            
    def render_typing_animation(self, text: str, delay: int = 50):
        """
        Render text with a typing animation
        
        Args:
            text: Text to animate
            delay: Delay between characters in ms
        """
        # Add JavaScript for typing animation
        st.markdown(f"""
        <div id="typing-text-{self.terminal_id}" class="system-response-{self.terminal_id}"></div>
        
        <script>
            const text = `{text}`;
            const typingElement = document.getElementById('typing-text-{self.terminal_id}');
            let i = 0;
            
            function typeWriter() {{
                if (i < text.length) {{
                    typingElement.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, Math.random() * {delay} + {delay/2});
                }} else {{
                    const cursor = document.createElement('span');
                    cursor.className = 'terminal-cursor-{self.terminal_id}';
                    typingElement.appendChild(cursor);
                }}
            }}
            
            setTimeout(typeWriter, 200);
        </script>
        """, unsafe_allow_html=True)
    
    def render_command_history(self):
        """Render the command history in the terminal"""
        if not self.command_history:
            return
            
        st.markdown(f"<div class='system-response-{self.terminal_id}'>Command History:</div>", unsafe_allow_html=True)
        
        for i, cmd in enumerate(reversed(self.command_history[-10:])):
            st.markdown(f"""
            <div class='user-command-{self.terminal_id}'>
                <span style="color: gray;">[{len(self.command_history) - i}]</span>
                <span class="terminal-prompt-{self.terminal_id}"></span>
                {cmd}
            </div>
            """, unsafe_allow_html=True)
    
    def set_theme(self, theme_colors: Dict[str, str]):
        """
        Update the terminal theme colors
        
        Args:
            theme_colors: Dictionary with primary, background, and text colors
        """
        self.theme_colors = theme_colors
        self._setup_css() 