"""
Security utilities for TRILOGY Brain
"""
import re
import html
import logging
from typing import Dict, Any, List, Optional
from functools import wraps
import time
import jwt
import secrets

logger = logging.getLogger(__name__)

def sanitize_input(input_text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        input_text: User input text
        
    Returns:
        Sanitized text
    """
    if not isinstance(input_text, str):
        return ""
        
    # Remove any potential script or iframe tags
    sanitized = re.sub(r'<script.*?>.*?</script>', '', input_text, flags=re.DOTALL)
    sanitized = re.sub(r'<iframe.*?>.*?</iframe>', '', sanitized, flags=re.DOTALL)
    
    # Escape HTML entities
    sanitized = html.escape(sanitized)
    
    return sanitized

def rate_limit(max_calls: int = 30, period: int = 60):
    """
    Rate limiting decorator for API endpoints
    
    Args:
        max_calls: Maximum number of calls allowed in the period
        period: Time period in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func):
        # Store call history
        call_history = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            
            # Remove expired entries
            while call_history and call_history[0] < current_time - period:
                call_history.pop(0)
                
            # Check if rate limit exceeded
            if len(call_history) >= max_calls:
                logger.warning(f"Rate limit exceeded: {max_calls} calls per {period}s")
                raise Exception(f"Rate limit exceeded. Please try again in {int(period - (current_time - call_history[0]))} seconds")
                
            # Add current call to history
            call_history.append(current_time)
            
            # Execute the function
            return func(*args, **kwargs)
            
        return wrapper
    return decorator

# JWT Authentication
JWT_SECRET = secrets.token_hex(32)  # Generate a secure secret key

def generate_auth_token(user_id: str, expiration: int = 3600) -> str:
    """
    Generate a JWT authentication token
    
    Args:
        user_id: User identifier
        expiration: Token expiration time in seconds
        
    Returns:
        JWT token
    """
    payload = {
        'user_id': user_id,
        'exp': time.time() + expiration
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_auth_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT authentication token
    
    Args:
        token: JWT token
        
    Returns:
        Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        return None 