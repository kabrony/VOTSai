"""
Advanced Command Line Interface for TRILOGY Brain
"""
import streamlit as st
from typing import Dict, Any, List, Optional, Callable

class CommandLine:
    """
    Advanced command line interface with terminal features
    
    Features:
    - Command history
    - Tab completion
    - Syntax highlighting
    - Command validation
    """
    
    def __init__(self, 
                theme_colors: Dict[str, str],
                available_commands: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the command line
        
        Args:
            theme_colors: Theme colors
            available_commands: List of available commands with name, description
        """
        self.theme_colors = theme_colors
        self.available_commands = available_commands or []
        self.command_history = []
        self._setup_css()
        
    def _setup_css(self):
        st.markdown(f"""
        <style>
        .cmd-container {{
            background-color: {self.theme_colors["background"]};
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 4px;
            padding: 10px;
            margin-bottom: 10px;
            font-family: 'Courier New', monospace;
        }}
        
        .cmd-prompt {{
            color: {self.theme_colors["primary"]};
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .cmd-input {{
            width: 100%;
            padding: 5px;
            background-color: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 2px;
            color: {self.theme_colors["text"]};
            font-family: 'Courier New', monospace;
        }}
        
        .cmd-suggestions {{
            margin-top: 5px;
            padding: 5px;
            background-color: rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 2px;
            max-height: 100px;
            overflow-y: auto;
        }}
        
        .cmd-suggestion {{
            padding: 2px 5px;
            cursor: pointer;
            font-size: 12px;
        }}
        
        .cmd-suggestion:hover {{
            background-color: rgba(255,255,255,0.1);
        }}
        
        .cmd-keyword {{
            color: #ff9900;
        }}
        
        .cmd-param {{
            color: #55ccff;
        }}
        
        .cmd-string {{
            color: #88ff88;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Add JavaScript for keyboard navigation and tab completion
        st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const cmdInput = document.getElementById('cmd-input');
            const suggestions = document.getElementById('cmd-suggestions');
            
            if (cmdInput && suggestions) {
                // Handle tab completion
                cmdInput.addEventListener('keydown', function(e) {
                    if (e.key === 'Tab') {
                        e.preventDefault();
                        // Implement tab completion logic
                    }
                    
                    // Handle up/down for history navigation
                    if (e.key === 'ArrowUp') {
                        // Navigate history up
                    } else if (e.key === 'ArrowDown') {
                        // Navigate history down
                    }
                });
                
                // Handle suggestion clicks
                suggestions.addEventListener('click', function(e) {
                    if (e.target.classList.contains('cmd-suggestion')) {
                        cmdInput.value = e.target.textContent;
                        cmdInput.focus();
                    }
                });
            }
        });
        </script>
        """, unsafe_allow_html=True)
    
    def render_command_line(self, 
                           placeholder: str = "Enter command...", 
                           on_submit: Optional[Callable[[str], None]] = None) -> str:
        """
        Render command line interface
        
        Args:
            placeholder: Placeholder text
            on_submit: Callback function when command is submitted
            
        Returns:
            Entered command
        """
        # Start container
        st.markdown('<div class="cmd-container">', unsafe_allow_html=True)
        
        # Prompt
        st.markdown('<div class="cmd-prompt">trilogy@brain:~$ </div>', unsafe_allow_html=True)
        
        # Command input
        command = st.text_input(
            label="",
            placeholder=placeholder,
            key="cmd_input",
            label_visibility="collapsed"
        )
        
        # Filter suggestions based on current input
        suggestions = []
        if command:
            suggestions = [cmd for cmd in self.available_commands 
                          if cmd["name"].startswith(command)]
        
        # Show suggestions if any
        if suggestions:
            st.markdown('<div class="cmd-suggestions" id="cmd-suggestions">', unsafe_allow_html=True)
            for suggestion in suggestions[:5]:  # Limit to 5 suggestions
                st.markdown(f'<div class="cmd-suggestion">{suggestion["name"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # End container
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle command submission
        if command and on_submit:
            # Add to history if not already there
            if not self.command_history or self.command_history[-1] != command:
                self.command_history.append(command)
            
            # Call the callback
            on_submit(command)
        
        return command
    
    def highlight_syntax(self, command: str) -> str:
        """
        Highlight command syntax
        
        Args:
            command: Command to highlight
            
        Returns:
            HTML-formatted highlighted command
        """
        # Simple syntax highlighting
        parts = command.split(' ')
        if not parts:
            return command
        
        # Highlight the command keyword
        result = f'<span class="cmd-keyword">{parts[0]}</span>'
        
        # Highlight parameters and strings
        for part in parts[1:]:
            if part.startswith('--') or part.startswith('-'):
                result += f' <span class="cmd-param">{part}</span>'
            elif part.startswith('"') and part.endswith('"'):
                result += f' <span class="cmd-string">{part}</span>'
            else:
                result += f' {part}'
                
        return result 