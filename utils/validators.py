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
            
        if len(query) > 4000:
            return False, f"Query too long ({len(query)} chars). Maximum is 4000 chars."
            
        # Check for potential injection patterns
        injection_patterns = [
            r"(\{|\[)%.*%(\}|\])",  # Format injection
            r"(__.*__)",  # Dunder method calls
            r"(exec|eval|compile)\s*\(",  # Code execution
            r"(os|subprocess|sys)\.",  # System modules
            r"<!--.*-->",  # HTML comments that might be used for XSS
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, query):
                logger.warning(f"Potentially unsafe query detected: {query[:100]}...")
                return False, "Query contains potentially unsafe patterns."
                
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
        """Sanitize user query for safe storage and display."""
        # Trim whitespace
        query = query.strip()
        
        # HTML escape for XSS prevention
        query = html.escape(query)
        
        return query
        
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
        """Validate model parameters for safety and correctness."""
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
        
    @staticmethod
    def validate_file_path(path: str) -> Tuple[bool, Optional[str]]:
        """Validate file path to prevent directory traversal."""
        if not path:
            return False, "Path cannot be empty."
            
        # Check for traversal attempts
        if ".." in path or path.startswith("/") or ":" in path:
            logger.warning(f"Potential path traversal attempt: {path}")
            return False, "Invalid file path. Relative paths from current directory only."
            
        # Check for unsafe characters
        if re.search(r"[<>|&;$]", path):
            return False, "Path contains invalid characters."
            
        return True, None 