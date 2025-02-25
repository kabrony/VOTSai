"""
Cursor API Integration for TRILOGY Brain

Client for interacting with AI models via Cursor-compatible APIs
"""
import os
import requests
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class CursorAPIClient:
    """
    Client for interacting with AI models via Cursor-compatible APIs
    
    Supports:
    - DeepSeek API integration
    - Claude API integration
    - Other OpenAI-compatible APIs
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("CURSOR_API_KEY")
        self.base_url = base_url or "https://api.deepseek.com/v1"
        
    def query(self, 
             prompt: str, 
             model: str = "deepseek-chat", 
             system_prompt: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Query an AI model via Cursor-compatible API
        
        Args:
            prompt: User prompt
            model: Model name to use
            system_prompt: System instructions
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response dictionary
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                f"{self.base_url}/chat/completions", 
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            return {
                "content": result["choices"][0]["message"]["content"],
                "model": result["model"],
                "tokens": {
                    "prompt": result["usage"]["prompt_tokens"],
                    "completion": result["usage"]["completion_tokens"],
                    "total": result["usage"]["total_tokens"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error querying Cursor API: {e}")
            return {
                "error": str(e),
                "content": f"Sorry, I encountered an error: {str(e)}"
            }
    
    def analyze_code(self, 
                    code: str, 
                    instructions: str = "Analyze this code and provide suggestions") -> Dict[str, Any]:
        """
        Analyze code using the API
        
        Args:
            code: Code to analyze
            instructions: Specific instructions for the analysis
            
        Returns:
            Analysis results
        """
        system_prompt = """You are an expert code analyst. Analyze the provided code and provide insights on:
1. Code quality and style
2. Potential bugs or issues
3. Performance optimizations
4. Security concerns
5. Specific improvements with code examples

Be specific and provide actionable recommendations."""
        
        prompt = f"{instructions}\n\n```\n{code}\n```"
        
        return self.query(
            prompt=prompt,
            model="deepseek-coder",
            system_prompt=system_prompt,
            temperature=0.3
        ) 