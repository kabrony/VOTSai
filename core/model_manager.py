import logging
from typing import Dict, Any

# Import your model classes
from core.claude_api import ClaudeAPI
from core.deepseek_api import DeepSeekAPI
from core.perplexity_api import PerplexityAPI
from core.local_models import LocalOllamaModel

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages access to different AI models"""
    
    def __init__(self):
        # Initialize available models
        self.models = {
            "Claude API": ClaudeAPI(),
            "DeepSeek API": DeepSeekAPI(),
            "Perplexity API": PerplexityAPI(),
            "Local DeepSeek": LocalOllamaModel("deepseek-coder")
        }
        
        # Model caching settings
        self.cache_enabled = True
        self.cache = {}
        
        # Load balancing and fallbacks
        self.fallbacks = {
            "Claude API": ["DeepSeek API", "Local DeepSeek"],
            "DeepSeek API": ["Claude API", "Local DeepSeek"],
            "Perplexity API": ["Claude API", "DeepSeek API"],
            "Local DeepSeek": ["DeepSeek API", "Claude API"]
        }
        
        logger.info(f"ModelManager initialized with {len(self.models)} models")
    
    def get_model(self, model_name: str):
        """
        Get a model by name, with fallback if not available
        """
        if model_name in self.models:
            return self.models[model_name]
        
        # If model not found, use first available fallback
        logger.warning(f"Model {model_name} not found, trying fallbacks")
        for fallback in self.fallbacks.get(model_name, []):
            if fallback in self.models:
                logger.info(f"Using {fallback} as fallback for {model_name}")
                return self.models[fallback]
        
        # If all fallbacks fail, raise exception
        logger.error(f"No available model found for {model_name} or its fallbacks")
        raise ValueError(f"No available model for {model_name}")
    
    def add_model(self, name: str, model):
        """
        Add a new model to the manager
        """
        self.models[name] = model
        logger.info(f"Added new model: {name}")
        
    def remove_model(self, name: str):
        """
        Remove a model from the manager
        """
        if name in self.models:
            del self.models[name]
            logger.info(f"Removed model: {name}")
    
    def get_available_models(self):
        """
        Get a list of all available models
        """
        return list(self.models.keys())
    
    def clear_cache(self):
        """
        Clear the model response cache
        """
        self.cache = {}
        logger.info("Model cache cleared") 