"""
Interactive Documentation Component for TRILOGY Brain
"""
import streamlit as st
from typing import Dict, List
import os
import json
import markdown

class DocsViewer:
    def __init__(self, docs_dir: str = "docs/generated"):
        self.docs_dir = docs_dir
        self._setup_css()
        
    def _setup_css(self):
        """Set up custom styling for documentation"""
        st.markdown("""
        <style>
        .docs-nav {
            background-color: #1a1a1a;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .docs-content {
            background-color: #0e1117;
            padding: 20px;
            border-radius: 5px;
            border-left: 3px solid #00f2ff;
        }
        .docs-example {
            background-color: #1c1c1c;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        /* More styling */
        </style>
        """, unsafe_allow_html=True)
    
    def render(self):
        """Render the interactive documentation viewer"""
        st.markdown("<h1>📚 TRILOGY Brain Documentation</h1>", unsafe_allow_html=True)
        
        # Create tabs for different documentation types
        doc_tabs = st.tabs(["User Guide", "API Reference", "Interactive Examples", "Architecture"])
        
        with doc_tabs[0]:
            self._render_user_guide()
            
        with doc_tabs[1]:
            self._render_api_reference()
            
        with doc_tabs[2]:
            self._render_interactive_examples()
            
        with doc_tabs[3]:
            self._render_architecture() 