import os
import time
import requests
import asyncio
import logging
import json

logger = logging.getLogger(__name__)

class ClaudeAPI:
    def __init__(self):
        self.name = "Claude API"
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-5-sonnet-20240620"
    
    async def query(self, query: str, timeout: int = 60, memory_context: str = "", web_context: str = "", tools=None, context=None, temperature: float = 0.7):
        """
        Call the Claude API to generate a response.
        
        Args:
            query: The user's query
            timeout: Maximum time to wait for response
            memory_context: Previous conversation context
            web_context: Additional web search context
            tools: Optional tools (not used by Claude API yet)
            context: Additional context (not used by Claude API yet)
            temperature: Controls randomness (0.0 to 1.0)
            
        Returns:
            Dict containing the response and metadata
        """
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Build system prompt
        system_message = "You are Claude, a helpful AI assistant powered by Anthropic. Use your thinking capability to provide detailed reasoning and analysis."
        if memory_context:
            system_message += f"\n\nMemory Context: {memory_context}"
        
        # Build full query
        full_query = query
        if web_context:
            full_query = f"{query}\n\nWeb Search Results: {web_context}"
        
        # Prepare API request
        payload = {
            "model": self.model,
            "max_tokens": 1500,
            "temperature": temperature,
            "system": system_message,
            "messages": [
                {"role": "user", "content": full_query}
            ]
        }
        
        try:
            # Make the API request
            start_time = time.time()
            logger.info(f"Sending request to Claude 3.7 Sonnet")
            
            # Execute request in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(
                    self.api_url, 
                    headers=headers,
                    json=payload,
                    timeout=timeout
                )
            )
            response.raise_for_status()
            
            # Parse the response JSON
            result = response.json()
            end_time = time.time()
            latency = end_time - start_time
            
            # Log the response structure for debugging
            logger.info(f"Claude API response keys: {list(result.keys())}")
            
            # Use join() method to safely combine text parts
            answer_parts = []
            
            # Process content if it exists and is a list
            if "content" in result and isinstance(result["content"], list):
                for block in result["content"]:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = block.get("text", "")
                        # Check if text is a string
                        if isinstance(text, str):
                            answer_parts.append(text)
                        # Check if text is a list
                        elif isinstance(text, list):
                            # Convert list items to strings and join them
                            answer_parts.append(" ".join(str(item) for item in text))
                        # Handle any other type by converting to string
                        else:
                            answer_parts.append(str(text))
                    # Handle thinking blocks if present
                    elif isinstance(block, dict) and block.get("type") == "thinking":
                        thinking_text = block.get("text", "")
                        if thinking_text:
                            answer_parts.append(f"\n\n**Thinking Process:**\n{thinking_text}")
            
            # Join all parts with spaces (safe way to concatenate)
            answer = " ".join(answer_parts)
            
            # Provide a fallback if we couldn't extract any text
            if not answer:
                logger.error(f"Failed to extract text from Claude response. Keys: {list(result.keys())}")
                # Include partial response in the log for debugging
                try:
                    logger.error(f"Partial response: {json.dumps(result)[:300]}...")
                except:
                    logger.error("Could not serialize response for logging")
                
                answer = "Error: Could not extract response from Claude API."
            
            # Estimate tokens
            input_tokens = len(full_query.split()) + len(system_message.split())
            output_tokens = len(answer.split())
            
            # Build the response
            return {
                "answer": answer,
                "model": f"Claude 3.7 Sonnet",
                "latency": latency,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Claude API error: {error_msg}")
            
            # Log response details if available
            if hasattr(e, 'response') and e.response:
                try:
                    error_text = e.response.text
                    logger.error(f"Response text: {error_text}")
                except:
                    pass
            
            # Return error information
            return {
                "answer": f"Error calling Claude 3.7 Sonnet API: {error_msg}",
                "model": f"Claude 3.7 Sonnet - Error",
                "latency": 0,
                "input_tokens": input_tokens if 'input_tokens' in locals() else 0,
                "output_tokens": 0
            } 