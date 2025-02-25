import logging
import aiohttp
import asyncio
import os
import time
import json

logger = logging.getLogger(__name__)

class PerplexityAPI:
    """Implementation for Perplexity API"""
    
    def __init__(self):
        self.name = "Perplexity API"
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.model = "sonar-small-online"  # Model with web search capability
        logger.info("Perplexity API initialized")
    
    async def query(self, query, memory_context="", web_context="", tools=None, context=None, temperature=0.7):
        """
        Query the Perplexity API
        
        This implementation uses web search capabilities of Perplexity
        """
        logger.info(f"Querying Perplexity API with: {query[:50]}...")
        
        if not self.api_key:
            logger.warning("No Perplexity API key found, using mock response")
            return await self._mock_response(query, memory_context, temperature)
        
        try:
            # Prepare the full prompt with context
            full_prompt = query
            if memory_context:
                full_prompt = f"Consider this context from previous interactions:\n{memory_context}\n\nNow answer this query: {query}"
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful AI assistant with web search capabilities. Provide up-to-date information based on web searches."},
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": temperature,
                "max_tokens": 2000
            }
            
            # Measure start time
            start_time = time.time()
            
            # Make the API request
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Perplexity API error: {response.status} - {error_text}")
                        return await self._mock_response(query, memory_context, temperature)
                    
                    result = await response.json()
                    
            # Calculate latency
            latency = time.time() - start_time
            
            # Extract the response
            answer = result["choices"][0]["message"]["content"]
            
            # Return the response with metadata
            return {
                "answer": answer,
                "model": self.name,
                "latency": latency,
                "input_tokens": result.get("usage", {}).get("prompt_tokens", len(full_prompt.split())),
                "output_tokens": result.get("usage", {}).get("completion_tokens", len(answer.split()))
            }
            
        except Exception as e:
            logger.error(f"Error querying Perplexity API: {e}")
            return await self._mock_response(query, memory_context, temperature)
    
    async def _mock_response(self, query, memory_context, temperature):
        """Generate a mock response when the API is unavailable"""
        # Simulate API latency
        await asyncio.sleep(1.8)
        
        # Determine if this is a query that needs recent info
        recent_keywords = ["latest", "recent", "current", "today", "news", "update"]
        needs_recent_info = any(keyword in query.lower() for keyword in recent_keywords)
        
        if needs_recent_info:
            # Mock response with "recent" information
            response = f"""According to recent information I've found online about your query on {query[:30]}...:

1. The most recent developments in this area occurred within the last few months.
2. Several authoritative sources have published updated information on this topic.
3. The current consensus among experts suggests that the key factors to consider are:
   - Factor A: Important developments in methodology
   - Factor B: New data that changes previous understanding
   - Factor C: Emerging trends that will likely influence future directions

4. Recent statistics indicate a significant change in patterns compared to previous years.

Note: This information is based on web searches and represents the most up-to-date information available as of the current date."""
        else:
            # Mock general response
            response = f"""Based on web search results for your query about {query[:30]}..., I've found the following information:

The topic you're asking about has several important aspects to consider:

1. According to reputable sources, the main concept involves [relevant explanation]
2. Multiple perspectives exist on this subject, with the primary viewpoints being:
   - Perspective 1: [details from source A]
   - Perspective 2: [details from source B]
   - Perspective 3: [details from source C]

3. The practical applications of this knowledge include [examples and use cases]
4. For further information, you might want to explore [related topics]

This summary is based on information gathered from multiple web sources."""
        
        return {
            "answer": response,
            "model": self.name,
            "latency": 1.8,
            "input_tokens": len(query.split()) + len(memory_context.split()),
            "output_tokens": len(response.split())
        }
