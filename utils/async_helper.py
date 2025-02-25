"""
Async Helper Utilities for TRILOGY Brain

Provides tools for managing asyncio event loops with Streamlit.
"""
import asyncio
import logging
import threading
from typing import Any, Callable, Coroutine, TypeVar, cast

logger = logging.getLogger(__name__)

T = TypeVar('T')

class AsyncHelper:
    """
    Helper class to manage asyncio event loops with Streamlit
    
    Streamlit runs in its own thread, which causes issues with asyncio's
    event loop. This class provides utilities to properly manage event loops
    across threads.
    """
    
    @staticmethod
    def get_or_create_event_loop():
        """
        Get the current event loop or create a new one if it doesn't exist
        
        Returns:
            asyncio.AbstractEventLoop: The event loop
        """
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return loop
            raise
    
    @staticmethod
    def run_async(coro: Coroutine[Any, Any, T]) -> T:
        """
        Run a coroutine in the current thread
        
        Args:
            coro: The coroutine to run
            
        Returns:
            The result of the coroutine
        """
        loop = AsyncHelper.get_or_create_event_loop()
        return loop.run_until_complete(coro)
    
    @staticmethod
    def run_sync(func: Callable[..., Coroutine[Any, Any, T]], *args, **kwargs) -> T:
        """
        Run an async function synchronously
        
        Args:
            func: The async function to run
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            The result of the function
        """
        return AsyncHelper.run_async(func(*args, **kwargs)) 