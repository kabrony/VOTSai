# ~/VOTSai/handlers/web.py
import aiohttp
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

async def crawl_url(url: str, timeout: int) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                return soup.get_text()
        except Exception as e:
            logger.error(f"Crawl failed for {url}: {e}")
            raise
