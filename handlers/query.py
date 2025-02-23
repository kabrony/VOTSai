# ~/VOTSai/handlers/query.py
import re
import json
from time import time
from typing import Dict, Any, Deque
from core.models import AIModel
from utils.helpers import format_response
from handlers.web import crawl_url
import logging

logger = logging.getLogger(__name__)

async def handle_general_query(query: str, timeout: int, memory_context: str, start_time: float, model: AIModel, web_priority: bool, temperature: float, share_format: str) -> Dict[str, Any]:
    try:
        web_context = await model.fetch_web_context(query, timeout) if web_priority else ""
        result = await model.query(query, timeout, memory_context, web_context, temperature)
        latency = time() - start_time
        actions_used = 1
        model_reasoning = "Web-enabled query" if web_priority else "General reasoning"
        final_answer = format_response(query, {**result, 'latency': latency, 'model_name': model.name, 'actions': actions_used, 'model_reasoning': model_reasoning}, share_format)
        return {**result, 'final_answer': final_answer, 'latency': latency, 'model_name': model.name, 'actions': actions_used, 'query_type': "general", 'model_reasoning': model_reasoning}
    except Exception as e:
        logger.error(f"General query failed with {model.name}: {e}")
        latency = time() - start_time
        final_answer = format_response(query, {'answer': f"Error: Query processing failed - {e}", 'latency': latency, 'model_name': model.name, 'input_tokens': 0, 'output_tokens': 0, 'actions': 1, 'model_reasoning': "Query processing failed"}, share_format)
        return {'final_answer': final_answer, 'latency': latency, 'model_name': model.name, 'actions': 1, 'query_type': "error", 'model_reasoning': "Query processing failed"}

async def handle_crawl_query(query: str, timeout: int, memory_context: str, start_time: float, model: AIModel, web_priority: bool, temperature: float, share_format: str) -> Dict[str, Any]:
    match = re.match(r'crawl\s+(.*)', query, re.IGNORECASE)
    if not match:
        latency = time() - start_time
        final_answer = format_response(query, {'answer': "Error: Invalid crawl command. Use 'crawl <url>'", 'latency': latency, 'model_name': model.name, 'input_tokens': 0, 'output_tokens': 0, 'actions': 0, 'model_reasoning': "Invalid syntax"}, share_format)
        return {'final_answer': final_answer, 'latency': latency, 'model_name': model.name, 'actions': 0, 'query_type': "error", 'model_reasoning': "Invalid syntax"}
    url = match.group(1).strip()
    try:
        text = await crawl_url(url, timeout)
        summary_query = f"Summarize this content (max 1000 chars): {text[:1000]}"
        web_context = await model.fetch_web_context(summary_query, timeout) if web_priority else ""
        result = await model.query(summary_query, timeout, memory_context, web_context, temperature)
        latency = time() - start_time
        actions_used = 1
        model_reasoning = "Web crawl summary"
        final_answer = format_response(query, {**result, 'latency': latency, 'model_name': model.name, 'actions': actions_used, 'model_reasoning': model_reasoning}, share_format)
        return {**result, 'final_answer': final_answer, 'latency': latency, 'model_name': model.name, 'actions': actions_used, 'query_type': "crawl", 'model_reasoning': model_reasoning}
    except Exception as e:
        logger.error(f"Crawl query failed: {e}")
        latency = time() - start_time
        final_answer = format_response(query, {'answer': f"Error: Crawl failed - {e}", 'latency': latency, 'model_name': model.name, 'input_tokens': 0, 'output_tokens': 0, 'actions': 1, 'model_reasoning': "Crawl failure"}, share_format)
        return {'final_answer': final_answer, 'latency': latency, 'model_name': model.name, 'actions': 1, 'query_type': "crawl", 'model_reasoning': "Crawl failure"}

async def handle_recall_query(query: str, conn: sqlite3.Connection, start_time: float, share_format: str) -> Dict[str, Any]:
    match = re.match(r'recall\s+(.*)', query, re.IGNORECASE)
    if not match:
        latency = time() - start_time
        final_answer = format_response(query, {'answer': "Error: Invalid recall command. Use 'recall <query>'", 'latency': latency, 'model_name': "Memory Recall", 'input_tokens': 0, 'output_tokens': 0, 'actions': 0, 'model_reasoning': "Invalid syntax"}, share_format)
        return {'final_answer': final_answer, 'latency': latency, 'model_name': "Memory Recall", 'actions': 0, 'query_type': "error", 'model_reasoning': "Invalid syntax"}
    recall_query = match.group(1).strip()
    memory_answer = get_relevant_memory(conn, recall_query)
    latency = time() - start_time
    final_answer = format_response(query, {'answer': memory_answer, 'latency': latency, 'model_name': "Memory Recall", 'input_tokens': 0, 'output_tokens': 0, 'actions': 1, 'model_reasoning': "Memory lookup"}, share_format)
    return {'final_answer': final_answer, 'latency': latency, 'model_name': "Memory Recall", 'actions': 1, 'query_type': "recall", 'model_reasoning': "Memory lookup"}

async def orchestrate_query(query: str, timeout: int, short_term_memory: Deque, conn: sqlite3.Connection, model: AIModel, web_priority: bool = True, temperature: float = 0.7, share_format: str = "Text") -> Dict[str, Any]:
    start_time = time()
    memory_context = f"Short-term: {json.dumps(list(short_term_memory)[-3:])}; Long-term: {get_relevant_memory(conn, query)}"
    try:
        if re.match(r'crawl\s+', query, re.IGNORECASE):
            result = await handle_crawl_query(query, timeout, memory_context, start_time, model, web_priority, temperature, share_format)
        elif re.match(r'recall\s+', query, re.IGNORECASE):
            result = await handle_recall_query(query, conn, start_time, share_format)
        else:
            result = await handle_general_query(query, timeout, memory_context, start_time, model, web_priority, temperature, share_format)
        update_memory(conn, query, result, short_term_memory)
        return result
    except Exception as e:
        logger.error(f"Orchestration failed with {model.name}: {e}")
        latency = time() - start_time
        final_answer = format_response(query, {'answer': f"Error: Orchestration failed - {e}", 'latency': latency, 'model_name': model.name, 'input_tokens': 0, 'output_tokens': 0, 'actions': 1, 'model_reasoning': "Orchestration failure"}, share_format)
        return {'final_answer': final_answer, 'latency': latency, 'model_name': model.name, 'actions': 1, 'query_type': "error", 'model_reasoning': "Orchestration failure"}
