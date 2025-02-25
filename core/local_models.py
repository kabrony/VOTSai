import logging
import asyncio
import time
import random

logger = logging.getLogger(__name__)

class LocalOllamaModel:
    """Stub implementation for local Ollama models"""
    
    def __init__(self, model_name):
        self.name = model_name  # Required for compatibility
        self.model_name = model_name
        logger.info(f"Initialized local model: {model_name}")
    
    async def query(self, query, memory_context="", web_context="", tools=None, context=None, temperature=0.7):
        """
        Stub implementation for querying local models
        In a real implementation, this would call Ollama
        """
        logger.info(f"Querying {self.model_name} with: {query[:50]}...")
        
        # Simulate processing time
        processing_time = 0.5 + random.random() * 2
        await asyncio.sleep(processing_time)
        
        # Build a mock response
        prefix = f"This is a response from {self.model_name}:\n\n"
        
        if "code" in query.lower() or "program" in query.lower():
            response = prefix + f"Here's an example related to your query about programming:\n\n```python\ndef example_function(parameter):\n    \"\"\"This is a sample function\"\"\"\n    return f'Result for {{parameter}}'\n```\n\nYou can use this code as a starting point."
        elif "data" in query.lower() or "analysis" in query.lower():
            response = prefix + f"To analyze data related to your query, I recommend the following approach:\n\n1. First, collect your data from a reliable source\n2. Clean the data to handle missing values\n3. Use appropriate statistical methods\n4. Visualize the results\n5. Draw conclusions based on your findings"
        else:
            response = prefix + f"Regarding your question about {query[:30]}..., there are several important points to consider. First, it's essential to understand the core concepts involved."
        
        # Return the mock response with metadata
        return {
            "answer": response,
            "model": self.model_name,
            "latency": processing_time,
            "input_tokens": len(query.split()) + len(memory_context.split()) + len(web_context.split() if web_context else []),
            "output_tokens": len(response.split())
        }