"""
UI Controls for Claude 3.7 Hybrid Reasoning
"""
import streamlit as st
import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HybridReasoningControls:
    """UI controls for Claude 3.7 Sonnet's hybrid reasoning capabilities"""
    
    def __init__(self, preferences_file: str = "data/hybrid_reasoning_prefs.json"):
        self.preferences_file = preferences_file
        self._load_preferences()
        
    def _load_preferences(self):
        """Load saved preferences or use defaults"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as f:
                    prefs = json.load(f)
                    self.thinking_mode = prefs.get("thinking_mode", "auto")
                    self.max_thinking_time = prefs.get("max_thinking_sec", 45)
                    self.reasoning_visibility = prefs.get("reasoning_visibility", "partial")
            else:
                self.thinking_mode = "auto"
                self.max_thinking_time = 45
                self.reasoning_visibility = "partial"
        except Exception as e:
            logger.error(f"Error loading hybrid reasoning preferences: {e}")
            self.thinking_mode = "auto"
            self.max_thinking_time = 45
            self.reasoning_visibility = "partial"
    
    def render_controls(self):
        """Render the hybrid reasoning controls in Streamlit"""
        st.sidebar.markdown("## Claude 3.7 Hybrid Reasoning")
        
        # Thinking mode selection
        self.thinking_mode = st.sidebar.radio(
            "Thinking Mode",
            options=["auto", "instant", "extended"],
            index=["auto", "instant", "extended"].index(self.thinking_mode),
            help="Auto: Claude decides when to use extended thinking\n"
                 "Instant: Quick responses without extended thinking\n"
                 "Extended: Always use extended thinking for complex problems"
        )
        
        # Max thinking time slider
        self.max_thinking_time = st.sidebar.slider(
            "Max Thinking Time (seconds)",
            min_value=1,
            max_value=120,
            value=self.max_thinking_time,
            help="Maximum time Claude can spend thinking (1-120 seconds)"
        )
        
        # Reasoning visibility
        self.reasoning_visibility = st.sidebar.radio(
            "Show Reasoning Process",
            options=["hidden", "partial", "full"],
            index=["hidden", "partial", "full"].index(self.reasoning_visibility),
            help="Hidden: Don't show thinking process\n"
                 "Partial: Show summary of thinking\n"
                 "Full: Show complete thinking process"
        )
        
        # Save preferences button
        if st.sidebar.button("Save Preferences"):
            self._save_preferences()
            st.sidebar.success("Preferences saved!")
            
        return {
            "thinking_mode": self.thinking_mode,
            "max_thinking_sec": self.max_thinking_time,
            "reasoning_visibility": self.reasoning_visibility
        }
        
    def _save_preferences(self):
        """Save hybrid reasoning preferences"""
        preferences = {
            "thinking_mode": self.thinking_mode,
            "max_thinking_sec": self.max_thinking_time,
            "reasoning_visibility": self.reasoning_visibility
        }
        
        try:
            os.makedirs(os.path.dirname(self.preferences_file), exist_ok=True)
            with open(self.preferences_file, 'w') as f:
                json.dump(preferences, f, indent=2)
            logger.info(f"Saved hybrid reasoning preferences to {self.preferences_file}")
        except Exception as e:
            logger.error(f"Error saving hybrid reasoning preferences: {e}") 