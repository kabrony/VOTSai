"""
Patches for Streamlit compatibility issues
"""
import sys
import types
import logging
from utils.async_helper import AsyncHelper

logger = logging.getLogger(__name__)

def apply_patches():
    """Apply all necessary patches for Streamlit compatibility"""
    # Patch torch._classes to avoid Streamlit file watcher errors
    if 'torch._classes' in sys.modules:
        logger.info("Applying torch._classes patch for Streamlit compatibility")
        sys.modules['torch._classes'].__path__ = types.SimpleNamespace(_path=[])
    
    # Initialize the asyncio event loop
    logger.info("Initializing asyncio event loop for Streamlit compatibility")
    AsyncHelper.get_or_create_event_loop()
    
    logger.info("All Streamlit compatibility patches applied") 