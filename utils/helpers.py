# ~/VOTSai/utils/helpers.py
import tiktoken
import base64
import json
import streamlit as st
import logging

logger = logging.getLogger(__name__)

def count_tokens(text: str, model_name: str) -> int:
    try:
        if "Perplexity" in model_name or "DeepSeek API" in model_name:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            return len(encoding.encode(text))
        return len(text.split()) + int(len(text) / 4)
    except Exception as e:
        logger.error(f"Token counting failed: {e}")
        return len(text.split())

def format_response(query: str, result: Dict[str, Any], share_format: str = "Text") -> str:
    try:
        base_content = {
            "Query": query,
            "Response": result['answer'],
            "Model Used": result['model_name'],
            "Latency": f"{result['latency']:.2f}s",
            "Input Tokens": result['input_tokens'],
            "Output Tokens": result['output_tokens'],
            "Actions Used": result['actions'],
            "Model Reasoning": result['model_reasoning'],
            "Analysis": result.get('analysis', "No additional analysis available.")
        }
        if share_format == "Markdown":
            formatted_content = "\n\n".join(f"**{k}**: {v}" for k, v in base_content.items())
        elif share_format == "JSON":
            formatted_content = json.dumps(base_content, indent=2)
        else:
            formatted_content = "\n\n".join(f"{k}: {v}" for k, v in base_content.items())
        encoded_content = base64.urlsafe_b64encode(formatted_content.encode()).decode()
        share_url = f"{st.get_option('browser.serverAddress')}?share={encoded_content}&format={share_format.lower()}"
        return f"{formatted_content}\n\n[Share this result]({share_url})"
    except Exception as e:
        logger.error(f"Response formatting failed: {e}")
        return f"Error formatting response: {e}"
