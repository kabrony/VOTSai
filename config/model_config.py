"""
Model Configuration

Contains configuration constants for AI models used in TRILOGY Brain.
"""

# Claude 3.7 Sonnet configuration
LATEST_MODEL = "claude-3.7-sonnet-20250224"
LATEST_API_VERSION = "2025-02-24"

# Model capabilities
MODEL_CAPABILITIES = {
    "claude-3.7-sonnet-20250224": {
        "hybrid_reasoning": True,
        "max_thinking_time": 120,  # seconds
        "max_tokens": 128000,  # beta limit
        "vision": True,
        "tool_use": True
    },
    "claude-3-opus-20240229": {
        "hybrid_reasoning": False,
        "max_tokens": 200000,
        "vision": True,
        "tool_use": True
    },
    "claude-3-sonnet-20240229": {
        "hybrid_reasoning": False,
        "max_tokens": 200000,
        "vision": True,
        "tool_use": True
    }
}

# Default settings
DEFAULT_THINKING_MODE = "auto"
DEFAULT_MAX_THINKING_SEC = 45
DEFAULT_REASONING_VISIBILITY = "partial"

# Cost per million tokens (in USD)
COST_PER_MILLION = {
    "claude-3.7-sonnet-20250224": {
        "input": 3.00,
        "output": 15.00,
        "thinking": 15.00  # Thinking tokens are billed as output
    },
    "claude-3-opus-20240229": {
        "input": 15.00,
        "output": 75.00
    },
    "claude-3-sonnet-20240229": {
        "input": 3.00,
        "output": 15.00
    }
}