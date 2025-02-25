# ~/VOTSai/core/models.py
import os
import asyncio
from typing import Dict, Any
from openai import AsyncOpenAI
import ollama
from tenacity import retry, wait_exponential, stop_after_attempt
from utils.helpers import count_tokens
from core.classifier import IntentClassifier
import logging
from core.claude_api import ClaudeAPI

logger = logging.getLogger(__name__)

class AIModel:
    def __init__(self, name: str):
        self.name = name

    async def query(self, query: str, timeout: int, memory_context: str, web_context: str = "", temperature: float = 0.7) -> Dict[str, Any]:
        raise NotImplementedError

    async def fetch_web_context(self, query: str, timeout: int, depth: int = 1) -> str:
        if not os.environ.get("PERPLEXITY_API_KEY"):
            return ""
        client = AsyncOpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")
        try:
            response = await client.chat.completions.create(
                model="sonar-pro",
                messages=[{"role": "user", "content": f"Fetch concise web data for {query} (depth={depth})."}],
                timeout=timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Web context fetch failed: {e}")
            return ""

class PerplexityAPI(AIModel):
    def __init__(self):
        super().__init__("Perplexity API")

    @retry(wait=wait_exponential(multiplier=1, min=2, max=30), stop=stop_after_attempt(5))
    async def query(self, query: str, timeout: int, memory_context: str, web_context: str = "", temperature: float = 0.7) -> Dict[str, Any]:
        client = AsyncOpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")
        try:
            response = await client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {"role": "system", "content": f"Provide concise, accurate answers with current web data. Memory: {memory_context}"},
                    {"role": "user", "content": f"{query}\nWeb Context: {web_context}" if web_context else query}
                ],
                temperature=temperature,
                timeout=timeout
            )
            answer = response.choices[0].message.content
            input_tokens = count_tokens(query + memory_context + web_context, self.name)
            output_tokens = count_tokens(answer, self.name)
            return {'answer': answer, 'input_tokens': input_tokens, 'output_tokens': output_tokens, 'analysis': ''}
        except Exception as e:
            logger.error(f"Perplexity API query failed: {e}")
            return {'answer': f"Error: Perplexity API failed - {e}", 'input_tokens': 0, 'output_tokens': 0, 'analysis': ''}

class DeepSeekAPI(AIModel):
    def __init__(self):
        super().__init__("DeepSeek API")

    @retry(wait=wait_exponential(multiplier=1, min=2, max=30), stop=stop_after_attempt(5))
    async def query(self, query: str, timeout: int, memory_context: str, web_context: str = "", temperature: float = 0.7) -> Dict[str, Any]:
        client = AsyncOpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        try:
            response = await client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": f"Provide detailed, reasoning-based answers. Memory: {memory_context}"},
                    {"role": "user", "content": f"{query}\nWeb Context: {web_context}" if web_context else query}
                ],
                temperature=temperature,
                timeout=timeout
            )
            answer = response.choices[0].message.content
            input_tokens = count_tokens(query + memory_context + web_context, self.name)
            output_tokens = count_tokens(answer, self.name)
            return {'answer': answer, 'input_tokens': input_tokens, 'output_tokens': output_tokens, 'analysis': ''}
        except Exception as e:
            logger.error(f"DeepSeek API query failed: {e}")
            return {'answer': f"Error: DeepSeek API failed - {e}", 'input_tokens': 0, 'output_tokens': 0, 'analysis': ''}

class LocalDeepSeek(AIModel):
    def __init__(self):
        super().__init__("Local DeepSeek")

    def query_sync(self, query: str, memory_context: str, web_context: str = "", temperature: float = 0.7) -> Dict[str, Any]:
        try:
            ollama.list()
            full_query = f"{query}\nWeb Context: {web_context}" if web_context else query
            response = ollama.chat(
                model="bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF:Q2_K",
                messages=[
                    {"role": "system", "content": f"Provide concise, well-formatted answers. Memory: {memory_context}"},
                    {"role": "user", "content": full_query}
                ],
                options={"temperature": temperature}
            )
            answer = response["message"]["content"]
            input_tokens = count_tokens(full_query + memory_context, self.name)
            output_tokens = count_tokens(answer, self.name)
            return {'answer': answer, 'input_tokens': input_tokens, 'output_tokens': output_tokens, 'analysis': 'Local analysis TBD'}
        except Exception as e:
            logger.error(f"Local DeepSeek query failed: {e}")
            return {'answer': f"Error: Local DeepSeek failed - {e}", 'input_tokens': 0, 'output_tokens': 0, 'analysis': ''}

    async def query(self, query: str, timeout: int, memory_context: str, web_context: str = "", temperature: float = 0.7) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.query_sync, query, memory_context, web_context, temperature)

class ModelFactory:
    def create_model(self, model_name: str) -> AIModel:
        models = {
            "Perplexity API": PerplexityAPI(),
            "DeepSeek API": DeepSeekAPI(),
            "Local DeepSeek": LocalDeepSeek(),
            "Claude API": ClaudeAPI()
        }
        return models.get(model_name, LocalDeepSeek())

    def select_model(self, query: str, user_selected: str, web_priority: bool, classifier: IntentClassifier) -> AIModel:
        if user_selected != "Auto":
            return self.create_model(user_selected)
        intent = classifier.predict(query)
        if web_priority or intent == "web_search":
            return self.create_model("Perplexity API")
        elif intent in ["technical", "conceptual"]:
            return self.create_model("DeepSeek API")
        return self.create_model("Local DeepSeek")