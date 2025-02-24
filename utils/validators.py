import re
import html
from typing import Dict, Any, Optional, Tuple, List
import logging
import urllib.parse

logger = logging.getLogger(__name__)

class Validator:
    """Input validation utility for VOTSai."""
    
    @staticmethod
    def validate_query(query: str) -> Tuple[bool, Optional[str]]:
        """Validate user query input."""
        if not query or not query.strip():
            return False, "Query cannot be empty."
            
        if len(query) > 8000:
            return False, f"Query too long ({len(query)} chars). Maximum is 8000 characters."
            
        return True, None
        
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, Optional[str]]:
        """Validate URL for web crawling."""
        if not url or not url.strip():
            return False, "URL cannot be empty."
            
        # Check if it's a valid URL
        url_pattern = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        
        if not url_pattern.match(url):
            return False, "Invalid URL format. Please enter a valid URL (e.g., https://example.com)."
            
        # Check for common security issues like localhost access (unless explicitly allowed)
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.netloc in ['localhost', '127.0.0.1'] and not url.startswith(('http://localhost:8501', 'http://127.0.0.1:8501')):
            return False, "Access to localhost is restricted."
            
        return True, None
        
    @staticmethod
    def sanitize_query(query: str) -> str:
        """Sanitize user query input."""
        # Remove potential HTML/script tags
        sanitized = html.escape(query)
        
        # Remove control characters except newlines and tabs
        sanitized = ''.join(c for c in sanitized if ord(c) >= 32 or c in '\n\t')
        
        return sanitized
        
    @staticmethod
    def validate_code(code: str) -> Tuple[bool, Optional[str]]:
        """Validate user-submitted code."""
        if not code or not code.strip():
            return False, "Code cannot be empty."
            
        if len(code) > 15000:
            return False, f"Code too long ({len(code)} chars). Maximum is 15000 characters."
            
        # Basic security check for malicious patterns
        dangerous_patterns = [
            r'os\.system\s*\(',
            r'subprocess\.(?:call|run|Popen)\s*\(',
            r'eval\s*\(',
            r'exec\s*\(',
            r'__import__\s*\('
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                return False, "Code contains potentially unsafe operations."
                
        return True, None
        
    @staticmethod
    def sanitize_output(output: str) -> str:
        """Sanitize model output."""
        # Escape HTML except for Markdown formatting
        # This is a simplified approach - for production you might want more sophisticated sanitization
        output = output.replace("<script", "&lt;script")
        
        # Strip control characters
        output = ''.join(c for c in output if ord(c) >= 32 or c in '\n\r\t')
        
        return output
        
    @staticmethod
    def validate_model_params(params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate model parameters."""
        if "temperature" in params:
            temp = params["temperature"]
            if not isinstance(temp, (int, float)) or temp < 0 or temp > 2:
                return False, "Temperature must be between 0 and 2."
                
        if "max_tokens" in params:
            max_tokens = params["max_tokens"]
            if not isinstance(max_tokens, int) or max_tokens < 1 or max_tokens > 32000:
                return False, "max_tokens must be between 1 and 32000."
                
        if "timeout" in params:
            timeout = params["timeout"]
            if not isinstance(timeout, (int, float)) or timeout < 1 or timeout > 300:
                return False, "Timeout must be between 1 and 300 seconds."
                
        return True, None 