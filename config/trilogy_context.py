"""
TRILOGY Brain Context Manager

Provides consistent system context to AI models throughout the application.
"""
import os
import yaml
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ContextManager:
    """Manages context information for AI models"""
    
    def __init__(self, config_path: str = "config/trilogy_context.yaml"):
        self.config_path = config_path
        self.context = self._load_context()
        
    def _load_context(self) -> Dict[str, Any]:
        """Load context from YAML file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                logger.warning(f"Context file not found: {self.config_path}")
                return self._create_default_context()
        except Exception as e:
            logger.error(f"Error loading context: {e}")
            return self._create_default_context()
            
    def _create_default_context(self) -> Dict[str, Any]:
        """Create default context structure"""
        return {
            "project_description": "TRILOGY Brain - Advanced AI orchestration system",
            "modes": {
                "base": {
                    "description": "Standard operation mode",
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                "enhanced": {
                    "description": "Advanced reasoning mode for complex problems",
                    "temperature": 0.3,
                    "max_tokens": 4000,
                    "thinking_mode": "extended" 
                }
            },
            "memory_rules": {
                "retention_policy": "Prioritize factual and technical information",
                "pruning_strategy": "Remove oldest and least relevant items first"
            },
            "web_crawling_rules": {
                "respect_robots_txt": True,
                "max_depth": 3,
                "max_pages_per_domain": 20,
                "follow_javascript_links": True
            }
        }
    
    def get_context(self, mode: str = "base") -> Dict[str, Any]:
        """Get context for a specific mode"""
        base_context = {
            "system": f"You are TRILOGY Brain, an advanced AI orchestration system. {self.context.get('project_description', '')}"
        }
        
        # Add mode-specific context
        mode_context = self.context.get("modes", {}).get(mode, {})
        base_context.update(mode_context)
        
        return base_context
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        """Update the context and save to file"""
        self.context.update(new_context)
        
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(self.context, f, default_flow_style=False)
            logger.info(f"Updated context saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving context: {e}") 