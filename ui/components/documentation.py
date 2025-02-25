"""
Interactive Documentation Component for TRILOGY Brain
"""
import streamlit as st
from typing import Dict, Any, List, Optional

class DocumentationSystem:
    """
    Interactive documentation system
    
    Features:
    - Search functionality
    - Interactive examples
    - Collapsible sections
    - Code highlighting
    """
    
    def __init__(self, theme_colors: Dict[str, str]):
        """
        Initialize documentation system
        
        Args:
            theme_colors: Theme colors
        """
        self.theme_colors = theme_colors
        self._setup_css()
        
        # Initialize session state
        if "doc_search_query" not in st.session_state:
            st.session_state.doc_search_query = ""
        if "doc_history" not in st.session_state:
            st.session_state.doc_history = []
    
    def _setup_css(self):
        st.markdown(f"""
        <style>
        .doc-container {{
            background-color: {self.theme_colors["background"]};
            color: {self.theme_colors["text"]};
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 5px;
            padding: 20px;
            font-family: 'Courier New', monospace;
        }}
        
        .doc-header {{
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid {self.theme_colors["primary"]};
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .doc-title {{
            font-size: 24px;
            color: {self.theme_colors["primary"]};
            font-weight: bold;
        }}
        
        .doc-search {{
            position: relative;
            width: 100%;
            max-width: 300px;
        }}
        
        .doc-nav {{
            margin-bottom: 20px;
            padding: 10px;
            background-color: rgba(0,0,0,0.2);
            border-radius: 5px;
            display: flex;
            align-items: center;
        }}
        
        .doc-nav-button {{
            background-color: rgba(0,0,0,0.3);
            color: {self.theme_colors["text"]};
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 3px;
            padding: 3px 8px;
            margin-right: 8px;
            cursor: pointer;
            font-size: 14px;
        }}
        
        .doc-nav-history {{
            flex-grow: 1;
            overflow-x: auto;
            white-space: nowrap;
            padding-bottom: 5px;
        }}
        
        .doc-nav-history-item {{
            display: inline-block;
            padding: 3px 8px;
            margin-right: 5px;
            background-color: rgba(0,0,0,0.2);
            border-radius: 3px;
            font-size: 12px;
            cursor: pointer;
        }}
        
        .doc-section {{
            margin-bottom: 20px;
        }}
        
        .doc-section-header {{
            font-size: 18px;
            color: {self.theme_colors["primary"]};
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .doc-code {{
            background-color: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 10px 0;
            font-family: monospace;
            position: relative;
        }}
        
        .doc-code-copy {{
            position: absolute;
            top: 5px;
            right: 5px;
            background-color: rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            border-radius: 3px;
            padding: 2px 5px;
            font-size: 10px;
            cursor: pointer;
        }}
        
        .doc-example {{
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 5px;
            margin: 15px 0;
            overflow: hidden;
        }}
        
        .doc-example-header {{
            background-color: rgba(0,0,0,0.3);
            padding: 8px 10px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .doc-example-content {{
            padding: 10px;
        }}
        
        .doc-toc {{
            background-color: rgba(0,0,0,0.2);
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        
        .doc-toc-title {{
            font-weight: bold;
            margin-bottom: 8px;
            color: {self.theme_colors["primary"]};
        }}
        
        .doc-toc-item {{
            padding: 3px 0 3px 15px;
            border-left: 2px solid rgba(255,255,255,0.1);
            margin-left: 5px;
            font-size: 14px;
        }}
        
        .doc-tag {{
            display: inline-block;
            padding: 2px 6px;
            background-color: rgba(0, 255, 65, 0.2);
            color: {self.theme_colors["primary"]};
            border-radius: 10px;
            font-size: 11px;
            margin-right: 5px;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Add JavaScript for code copy functionality
        st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Add code copy functionality
            document.querySelectorAll('.doc-code-copy').forEach(button => {
                button.addEventListener('click', function() {
                    const code = this.previousElementSibling.textContent;
                    navigator.clipboard.writeText(code).then(function() {
                        button.textContent = 'Copied!';
                        setTimeout(() => {
                            button.textContent = 'Copy';
                        }, 2000);
                    });
                });
            });
        });
        </script>
        """, unsafe_allow_html=True)
    
    def render_documentation(self, 
                            title: str, 
                            sections: List[Dict[str, Any]],
                            search_callback: Optional[Callable[[str], List[Dict[str, Any]]]] = None):
        """
        Render interactive documentation
        
        Args:
            title: Documentation title
            sections: List of documentation sections
            search_callback: Function to search documentation
        """
        st.markdown(f"""
        <div class="doc-container">
            <div class="doc-header">
                <div class="doc-title">{title}</div>
                <div class="doc-search">
                    <input type="text" placeholder="Search documentation..." id="doc-search-input">
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation bar with history
        st.markdown("""
        <div class="doc-nav">
            <div class="doc-nav-button" onclick="history.back()">← Back</div>
            <div class="doc-nav-button" onclick="history.forward()">Forward →</div>
            <div class="doc-nav-history">
        """, unsafe_allow_html=True)
        
        for item in st.session_state.doc_history[-5:]:  # Show last 5 items
            st.markdown(f"""
            <div class="doc-nav-history-item">{item}</div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Table of contents
        if len(sections) > 1:
            st.markdown("""
            <div class="doc-toc">
                <div class="doc-toc-title">Table of Contents</div>
            """, unsafe_allow_html=True)
            
            for section in sections:
                st.markdown(f"""
                <div class="doc-toc-item">{section["title"]}</div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Render each section
        for section in sections:
            self._render_section(section)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _render_section(self, section: Dict[str, Any]):
        """
        Render a documentation section
        
        Args:
            section: Section data with title, content, code, examples
        """
        st.markdown(f"""
        <div class="doc-section">
            <div class="doc-section-header">{section["title"]}</div>
        """, unsafe_allow_html=True)
        
        # Content
        if "content" in section:
            st.markdown(section["content"], unsafe_allow_html=True)
        
        # Code blocks
        if "code" in section and section["code"]:
            for code_block in section["code"]:
                language = code_block.get("language", "python")
                code = code_block.get("code", "")
                description = code_block.get("description", "")
                
                if description:
                    st.markdown(description)
                
                st.markdown(f"""
                <div class="doc-code">
                    <pre><code class="{language}">{code}</code></pre>
                    <div class="doc-code-copy">Copy</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Interactive examples
        if "examples" in section and section["examples"]:
            for example in section["examples"]:
                title = example.get("title", "Example")
                description = example.get("description", "")
                
                st.markdown(f"""
                <div class="doc-example">
                    <div class="doc-example-header">
                        <div>{title}</div>
                        <div>
                            <span class="doc-tag">Interactive</span>
                        </div>
                    </div>
                    <div class="doc-example-content">
                """, unsafe_allow_html=True)
                
                if description:
                    st.markdown(description)
                
                # Custom rendering for different example types
                if "type" in example:
                    if example["type"] == "code":
                        with st.echo():
                            exec(example.get("code", ""))
                    elif example["type"] == "form":
                        self._render_example_form(example)
                
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _render_example_form(self, example: Dict[str, Any]):
        """
        Render an interactive example form
        
        Args:
            example: Example data with fields and submit action
        """
        with st.form(f"example_form_{id(example)}"):
            form_data = {}
            
            # Render form fields
            for field in example.get("fields", []):
                field_type = field.get("type", "text")
                field_key = field.get("key", "")
                field_label = field.get("label", "")
                
                if field_type == "text":
                    form_data[field_key] = st.text_input(field_label)
                elif field_type == "number":
                    form_data[field_key] = st.number_input(field_label)
                elif field_type == "select":
                    form_data[field_key] = st.selectbox(
                        field_label, 
                        options=field.get("options", [])
                    )
            
            # Submit button
            submitted = st.form_submit_button("Run Example")
            
            if submitted:
                # Execute callback if provided
                if "callback" in example and callable(example["callback"]):
                    result = example["callback"](form_data)
                    st.write(result) 