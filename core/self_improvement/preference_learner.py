"""
User preference learning system for TRILOGY Brain
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
import json
import os
import time

class UserPreferenceLearner:
    """Learns user preferences to personalize responses"""
    
    def __init__(self, data_path: str = "data/preferences"):
        self.data_path = data_path
        self.logger = logging.getLogger("trilogy.preferences")
        os.makedirs(data_path, exist_ok=True)
        self.preferences = self._load_preferences()
        
    def record_preference(self, user_id: str, category: str, choice: str, 
                          strength: float = 1.0):
        """Record a user preference"""
        if user_id not in self.preferences:
            self.preferences[user_id] = {}
            
        if category not in self.preferences[user_id]:
            self.preferences[user_id][category] = {}
            
        if choice not in self.preferences[user_id][category]:
            self.preferences[user_id][category][choice] = 0
            
        # Update preference strength
        current_value = self.preferences[user_id][category][choice]
        # Apply exponential moving average
        self.preferences[user_id][category][choice] = (0.8 * current_value) + (0.2 * strength)
        
        # Save updated preferences
        self._save_preferences()
        
    def get_preference(self, user_id: str, category: str) -> Dict[str, float]:
        """Get user preferences for a category"""
        if user_id in self.preferences and category in self.preferences[user_id]:
            return self.preferences[user_id][category]
        return {} 