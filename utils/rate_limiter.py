import time
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Any
import threading
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiting utility to prevent API abuse."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RateLimiter, cls).__new__(cls)
            cls._init_instance()
        return cls._instance
    
    @classmethod
    def _init_instance(cls):
        """Initialize the instance."""
        cls._request_history = defaultdict(list)
        cls._token_usage = defaultdict(lambda: {"input": 0, "output": 0})
        
        cls._limits = {
            "default": {
                "requests_per_minute": 20,
                "requests_per_hour": 300,
                "requests_per_day": 1000,
                "input_tokens_per_day": 200000,
                "output_tokens_per_day": 50000
            }
        }
    
    def check_rate_limit(self, client_id: str = "default") -> Tuple[bool, Optional[str]]:
        """Check if a client is within rate limits."""
        with self._lock:
            self._clean_old_requests(client_id)
            
            # Get client limits (fall back to default if not set)
            limits = self._limits.get(client_id, self._limits["default"])
            
            # Get client history
            history = self._request_history[client_id]
            now = time.time()
            
            # Check requests per minute
            minute_ago = now - 60
            requests_last_minute = sum(1 for req in history if req["timestamp"] > minute_ago)
            if requests_last_minute >= limits["requests_per_minute"]:
                return False, f"Rate limit exceeded: {requests_last_minute}/{limits['requests_per_minute']} requests in the last minute"
                
            # Check requests per hour
            hour_ago = now - 3600
            requests_last_hour = sum(1 for req in history if req["timestamp"] > hour_ago)
            if requests_last_hour >= limits["requests_per_hour"]:
                return False, f"Rate limit exceeded: {requests_last_hour}/{limits['requests_per_hour']} requests in the last hour"
                
            # Check requests per day
            if len(history) >= limits["requests_per_day"]:
                return False, f"Rate limit exceeded: {len(history)}/{limits['requests_per_day']} requests in the last day"
                
            # Check token usage
            token_usage = self._token_usage[client_id]
            if token_usage["input"] >= limits["input_tokens_per_day"]:
                return False, f"Token limit exceeded: {token_usage['input']}/{limits['input_tokens_per_day']} input tokens today"
                
            if token_usage["output"] >= limits["output_tokens_per_day"]:
                return False, f"Token limit exceeded: {token_usage['output']}/{limits['output_tokens_per_day']} output tokens today"
                
            # Add this request to history
            self._request_history[client_id].append({
                "timestamp": now,
                "type": "request"
            })
            
            return True, None
    
    def track_token_usage(self, client_id: str, input_tokens: int, output_tokens: int) -> None:
        """Track token usage for a client."""
        with self._lock:
            self._token_usage[client_id]["input"] += input_tokens
            self._token_usage[client_id]["output"] += output_tokens
    
    def _clean_old_requests(self, client_id: str) -> None:
        """Remove requests older than 24 hours."""
        history = self._request_history[client_id]
        now = time.time()
        day_ago = now - 86400  # 24 hours in seconds
        
        # Reset token counts if needed (new day)
        if history and history[0]["timestamp"] < day_ago:
            self._token_usage[client_id] = {"input": 0, "output": 0}
        
        # Keep only requests from the last day
        self._request_history[client_id] = [req for req in history if req["timestamp"] > day_ago]
    
    def set_client_limits(self, client_id: str, limits: Dict[str, int]) -> None:
        """Set custom limits for a client."""
        with self._lock:
            # Ensure all required limits are present
            full_limits = dict(self._limits["default"])
            full_limits.update(limits)
            self._limits[client_id] = full_limits
    
    def get_usage_stats(self, client_id: str = "default") -> Dict[str, Any]:
        """Get usage statistics for a client."""
        with self._lock:
            self._clean_old_requests(client_id)
            history = self._request_history[client_id]
            now = time.time()
            
            minute_ago = now - 60
            hour_ago = now - 3600
            
            return {
                "requests": {
                    "last_minute": sum(1 for req in history if req["timestamp"] > minute_ago),
                    "last_hour": sum(1 for req in history if req["timestamp"] > hour_ago),
                    "last_day": len(history)
                },
                "tokens": {
                    "input": self._token_usage[client_id]["input"],
                    "output": self._token_usage[client_id]["output"],
                    "total": self._token_usage[client_id]["input"] + self._token_usage[client_id]["output"]
                }
            }
