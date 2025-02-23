# ~/VOTSai/handlers/web.py
import asyncio
from crawl4ai import AsyncWebCrawler
import logging

logger = logging.getLogger(__name__)

async def crawl_url(url: str, timeout: int) -> str:
    try:
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(
                url=url,
                bypass_cache=True,  # Ensure fresh crawl
                timeout=timeout * 1000,  # Convert seconds to milliseconds
                page_timeout=timeout * 1000,
            )
            if result.success:
                return result.html  # Return raw HTML (Crawl4AI cleans it)
            else:
                raise Exception(result.error_message or f"Failed to crawl {url}")
    except Exception as e:
        logger.error(f"Crawl failed for {url}: {e}")
        raise Exception(str(e))