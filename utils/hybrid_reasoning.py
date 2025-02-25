"""
Hybrid Reasoning Utilities for Claude 3.7 Sonnet

Provides tools for working with Claude 3.7's hybrid reasoning capabilities.
"""
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class HybridReasoningManager:
    """
    Manages hybrid reasoning settings for Claude 3.7 Sonnet
    
    Features:
    - Thinking mode selection
    - Thinking time configuration
    - Reasoning visibility control
    - Preset configurations for different use cases
    """
    
    # Available thinking modes
    THINKING_MODES = ["auto", "instant", "extended"]
    
    # Available reasoning visibility options
    VISIBILITY_OPTIONS = ["hidden", "partial", "full"]
    
    # Preset configurations for different use cases
    PRESETS = {
        "quick_response": {
            "thinking_mode": "instant",
            "max_thinking_sec": 1,
            "reasoning_visibility": "hidden"
        },
        "balanced": {
            "thinking_mode": "auto",
            "max_thinking_sec": 30,
            "reasoning_visibility": "partial"
        },
        "deep_analysis": {
            "thinking_mode": "extended",
            "max_thinking_sec": 60,
            "reasoning_visibility": "full"
        },
        "code_review": {
            "thinking_mode": "extended",
            "max_thinking_sec": 45,
            "reasoning_visibility": "full"
        },
        "creative": {
            "thinking_mode": "auto",
            "max_thinking_sec": 20,
            "reasoning_visibility": "hidden"
        }
    }
    
    @classmethod
    def get_preset(cls, preset_name: str) -> Dict[str, Any]:
        """
        Get a preset configuration by name
        
        Args:
            preset_name: Name of the preset
            
        Returns:
            Preset configuration dictionary
        """
        if preset_name not in cls.PRESETS:
            logger.warning(f"Unknown preset '{preset_name}', falling back to 'balanced'")
            preset_name = "balanced"
            
        return cls.PRESETS[preset_name].copy()
    
    @classmethod
    def validate_settings(cls, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize hybrid reasoning settings
        
        Args:
            settings: Hybrid reasoning settings
            
        Returns:
            Validated and normalized settings
        """
        validated = {}
        
        # Validate thinking mode
        if "thinking_mode" in settings:
            mode = settings["thinking_mode"]
            if mode not in cls.THINKING_MODES:
                logger.warning(f"Invalid thinking mode '{mode}', falling back to 'auto'")
                validated["thinking_mode"] = "auto"
            else:
                validated["thinking_mode"] = mode
        else:
            validated["thinking_mode"] = "auto"
            
        # Validate max thinking time
        if "max_thinking_sec" in settings:
            time_sec = settings["max_thinking_sec"]
            try:
                time_sec = int(time_sec)
                # Clamp to valid range
                time_sec = max(1, min(120, time_sec))
                validated["max_thinking_sec"] = time_sec
            except (ValueError, TypeError):
                logger.warning(f"Invalid max thinking time '{time_sec}', falling back to 30")
                validated["max_thinking_sec"] = 30
        else:
            validated["max_thinking_sec"] = 30
            
        # Validate reasoning visibility
        if "reasoning_visibility" in settings:
            visibility = settings["reasoning_visibility"]
            if visibility not in cls.VISIBILITY_OPTIONS:
                logger.warning(f"Invalid reasoning visibility '{visibility}', falling back to 'partial'")
                validated["reasoning_visibility"] = "partial"
            else:
                validated["reasoning_visibility"] = visibility
        else:
            validated["reasoning_visibility"] = "partial"
            
        return validated
    
    @classmethod
    def create_context(cls, 
                      query: str, 
                      thinking_mode: str = "auto",
                      max_thinking_sec: int = 30,
                      reasoning_visibility: str = "partial",
                      tools: List[Dict[str, Any]] = None,
                      codebase: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a context dictionary for Claude 3.7 query
        
        Args:
            query: The user's query
            thinking_mode: Thinking mode (auto, instant, extended)
            max_thinking_sec: Maximum thinking time in seconds (1-120)
            reasoning_visibility: Reasoning visibility (hidden, partial, full)
            tools: List of available tools
            codebase: GitHub URL for code context
            
        Returns:
            Context dictionary for Claude 3.7 query
        """
        context = {
            "query": query,
            "thinking_mode": thinking_mode,
            "max_thinking_sec": max_thinking_sec,
            "reasoning_visibility": reasoning_visibility
        }
        
        if tools:
            context["tools"] = tools
            
        if codebase:
            context["codebase"] = codebase
            
        return cls.validate_settings(context) 