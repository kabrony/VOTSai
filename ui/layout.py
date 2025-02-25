"""
Adaptive Layout System for TRILOGY Brain
"""
import streamlit as st
from typing import List, Dict, Any, Optional, Tuple

class AdaptiveLayout:
    """
    Responsive layout manager for TRILOGY Brain
    
    Features:
    - Responsive grid layouts
    - Dynamic component sizing
    - Layout state persistence
    """
    
    def __init__(self):
        """Initialize the layout manager"""
        # Initialize layout state
        if "layout_state" not in st.session_state:
            st.session_state.layout_state = {
                "sidebar_width": 300,
                "compact_mode": False,
                "layout_mode": "standard",  # standard, compact, expanded
                "hidden_components": []
            }
    
    def toggle_compact_mode(self):
        """Toggle compact mode on/off"""
        st.session_state.layout_state["compact_mode"] = not st.session_state.layout_state["compact_mode"]
    
    def set_layout_mode(self, mode: str):
        """
        Set the current layout mode
        
        Args:
            mode: Layout mode (standard, compact, expanded)
        """
        if mode in ["standard", "compact", "expanded"]:
            st.session_state.layout_state["layout_mode"] = mode
    
    def hide_component(self, component_id: str):
        """
        Hide a component by ID
        
        Args:
            component_id: Component ID to hide
        """
        if component_id not in st.session_state.layout_state["hidden_components"]:
            st.session_state.layout_state["hidden_components"].append(component_id)
    
    def show_component(self, component_id: str):
        """
        Show a previously hidden component
        
        Args:
            component_id: Component ID to show
        """
        if component_id in st.session_state.layout_state["hidden_components"]:
            st.session_state.layout_state["hidden_components"].remove(component_id)
    
    def is_component_visible(self, component_id: str) -> bool:
        """
        Check if a component is visible
        
        Args:
            component_id: Component ID to check
            
        Returns:
            True if visible, False if hidden
        """
        return component_id not in st.session_state.layout_state["hidden_components"]
    
    def responsive_grid(self, 
                       components: List[Dict[str, Any]], 
                       columns: int = 3, 
                       compact_columns: int = 1) -> List[st.container]:
        """
        Create a responsive grid layout
        
        Args:
            components: List of components with ID, title, content
            columns: Number of columns in standard mode
            compact_columns: Number of columns in compact mode
            
        Returns:
            List of column containers
        """
        # Determine actual columns based on mode
        if st.session_state.layout_state["compact_mode"]:
            actual_columns = compact_columns
        else:
            actual_columns = columns
        
        # Create columns
        cols = st.columns(actual_columns)
        
        # Place components in columns
        visible_components = [c for c in components 
                             if c["id"] not in st.session_state.layout_state["hidden_components"]]
        
        for i, component in enumerate(visible_components):
            col_index = i % actual_columns
            with cols[col_index]:
                st.subheader(component["title"])
                component["content"]()
        
        return cols
    
    def render_layout_controls(self):
        """Render layout control widgets"""
        with st.expander("Layout Settings", expanded=False):
            cols = st.columns(3)
            
            with cols[0]:
                if st.button("Standard View", use_container_width=True):
                    self.set_layout_mode("standard")
                    st.rerun()
            
            with cols[1]:
                if st.button("Compact View", use_container_width=True):
                    self.set_layout_mode("compact")
                    self.toggle_compact_mode()
                    st.rerun()
            
            with cols[2]:
                if st.button("Expanded View", use_container_width=True):
                    self.set_layout_mode("expanded")
                    st.session_state.layout_state["compact_mode"] = False
                    st.rerun()
            
            st.markdown("#### Visible Components")
            
            all_components = [
                {"id": "neural_interface", "name": "Neural Interface"},
                {"id": "system_monitor", "name": "System Monitor"},
                {"id": "memory_explorer", "name": "Memory Explorer"},
                {"id": "analytics", "name": "Analytics"},
                {"id": "plugins", "name": "Plugins"}
            ]
            
            for comp in all_components:
                cols = st.columns([4, 1])
                with cols[0]:
                    st.write(comp["name"])
                with cols[1]:
                    visible = self.is_component_visible(comp["id"])
                    if st.checkbox("Show", value=visible, key=f"visibility_{comp['id']}") != visible:
                        if visible:
                            self.hide_component(comp["id"])
                        else:
                            self.show_component(comp["id"])
                        st.rerun() 