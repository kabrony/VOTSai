# ~/VOTSai/agents/codeAgent.py
import os
from openai import AsyncOpenAI
import logging

logger = logging.getLogger(__name__)

async def analyze_code(code: str) -> str:
    client = AsyncOpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"Analyze this code and suggest improvements:\n{code}"}],
            timeout=60
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Code analysis failed: {e}")
        return f"Error: {e}"