import logging
from typing import Dict, Any, Optional, Callable, Tuple
import time
import threading

logger = logging.getLogger(__name__)

class ModelCache:
    """Singleton cache for AI models to prevent redundant initialization."""
    
    _instance = None
    _models = {}
    _last_used = {}
    _max_idle_time = 3600  # 1 hour
    _lock = threading.RLock()  # Reentrant lock for thread safety
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelCache, cls).__new__(cls)
        return cls._instance
        
    def get_model(self, name: str, creator_func: Callable, *args, **kwargs) -> Any:
        """Get a model from the cache or create it if not exists."""
        with self._lock:
            now = time.time()
            
            # If the model exists, update last used time and return it
            if name in self._models:
                self._last_used[name] = now
                logger.debug(f"Cache hit for model: {name}")
                return self._models[name]
                
            # Otherwise, create the model
            try:
                logger.info(f"Creating new model: {name}")
                model = creator_func(*args, **kwargs)
                self._models[name] = model
                self._last_used[name] = now
                return model
            except Exception as e:
                logger.error(f"Failed to create model {name}: {e}")
                raise
                
    def remove_model(self, name: str) -> bool:
        """Remove a model from the cache."""
        with self._lock:
            if name in self._models:
                # Get the model to clean up
                model = self._models[name]
                
                # Remove from dictionaries
                del self._models[name]
                del self._last_used[name]
                
                # Attempt to clean up resources
                try:
                    if hasattr(model, 'close'):
                        model.close()
                    logger.info(f"Removed model from cache: {name}")
                    return True
                except Exception as e:
                    logger.warning(f"Error cleaning up model {name}: {e}")
                    return True  # Still removed from cache even if cleanup failed
            return False
            
    def clean_cache(self, max_idle_time: int = None) -> int:
        """Remove models that haven't been used for max_idle_time seconds."""
        with self._lock:
            if max_idle_time is None:
                max_idle_time = self._max_idle_time
                
            now = time.time()
            to_remove = []
            removed = 0
            
            # Find idle models
            for name, last_used in self._last_used.items():
                if now - last_used > max_idle_time:
                    to_remove.append(name)
                    
            # Remove them from the cache
            for name in to_remove:
                if self.remove_model(name):
                    removed += 1
                
            return removed
        
    def clear_cache(self) -> int:
        """Clear all models from the cache."""
        with self._lock:
            count = len(self._models)
            self._models.clear()
            self._last_used.clear()
            logger.info(f"Cleared model cache ({count} models)")
            return count
            
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about cached models."""
        with self._lock:
            now = time.time()
            return {
                "model_count": len(self._models),
                "models": {
                    name: {
                        "idle_time": now - self._last_used.get(name, now),
                        "type": type(model).__name__
                    }
                    for name, model in self._models.items()
                }
            }
