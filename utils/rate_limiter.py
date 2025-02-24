import time
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
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
            
            history = self._request_history[client_id]
            now = time.time()
            
            minute_ago = now - 60
            hour_ago = now - 3600
            
            # Check request limits
            requests_last_minute = sum(1 for req in history if req["timestamp"] > minute_ago)
            requests_last_hour = sum(1 for req in history if req["timestamp"] > hour_ago)
            requests_last_day = len(history)
            
            limits = self._limits.get(client_id, self._limits["default"])
            
            if requests_last_minute >= limits["requests_per_minute"]:
                return False, f"Rate limit exceeded: {requests_last_minute} requests in the last minute. Please wait."
                
            if requests_last_hour >= limits["requests_per_hour"]:
                return False, f"Rate limit exceeded: {requests_last_hour} requests in the last hour. Please try later."
                
            if requests_last_day >= limits["requests_per_day"]:
                return False, f"Daily rate limit of {limits['requests_per_day']} requests exceeded. Please try again tomorrow."
                
            # Check token limits
            tokens = self._token_usage[client_id]
            if tokens["input"] > limits["input_tokens_per_day"]:
                return False, f"Daily input token limit exceeded ({tokens['input']}). Please try again tomorrow."
                
            if tokens["output"] > limits["output_tokens_per_day"]:
                return False, f"Daily output token limit exceeded ({tokens['output']}). Please try again tomorrow."
                
            return True, None
    
    def record_request(self, client_id: str, input_tokens: int = 0, output_tokens: int = 0) -> None:
        """Record a request for rate limiting purposes."""
        with self._lock:
            self._request_history[client_id].append({
                "timestamp": time.time(),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            })
            
            # Update token usage
            self._token_usage[client_id]["input"] += input_tokens
            self._token_usage[client_id]["output"] += output_tokens
    
    def _clean_old_requests(self, client_id: str) -> None:
        """Remove requests older than 1 day."""
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