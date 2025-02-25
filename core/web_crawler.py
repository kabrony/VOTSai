"""
Enhanced Web Crawler for TRILOGY Brain

Provides advanced web crawling capabilities with memory integration
"""
import aiohttp
import asyncio
import logging
import time
from typing import Dict, Any, List, Set
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import os
import json

logger = logging.getLogger(__name__)

class EnhancedWebCrawler:
    """Advanced web crawler with memory integration"""
    
    def __init__(self, memory_system=None, max_pages=20, max_depth=3, respect_robots=True):
        self.memory_system = memory_system
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.respect_robots = respect_robots
        self.visited = set()
        self.robots_cache = {}
        self.results = []
        
    async def crawl(self, start_url: str, query: str) -> Dict[str, Any]:
        """
        Crawl a website starting from the given URL
        
        Args:
            start_url: The URL to start crawling from
            query: The query to search for in the content
            
        Returns:
            Dictionary with crawling results
        """
        self.visited = set()
        self.results = []
        
        try:
            start_time = time.time()
            
            # Parse the domain for robots.txt checking
            domain = urlparse(start_url).netloc
            
            # Check robots.txt if enabled
            if self.respect_robots:
                allowed = await self._check_robots_txt(domain, start_url)
                if not allowed:
                    logger.warning(f"URL {start_url} is disallowed by robots.txt")
                    return {
                        "success": False,
                        "error": "URL disallowed by robots.txt",
                        "url": start_url
                    }
            
            # Start the crawl
            await self._crawl_page(start_url, query, depth=0)
            
            # Save results to memory if available
            if self.memory_system and self.results:
                self._save_to_memory(query, self.results)
            
            return {
                "success": True,
                "url": start_url,
                "pages_crawled": len(self.visited),
                "query": query,
                "execution_time": time.time() - start_time,
                "results": self.results[:10]  # Return top 10 results
            }
            
        except Exception as e:
            logger.error(f"Error crawling {start_url}: {str(e)}")
            return {
                "success": False,
                "url": start_url,
                "error": str(e)
            }
    
    async def _crawl_page(self, url: str, query: str, depth: int = 0) -> None:
        """
        Crawl a single page and its links
        
        Args:
            url: URL to crawl
            query: Query to search for
            depth: Current depth level
        """
        # Check if we've reached the limits
        if url in self.visited or len(self.visited) >= self.max_pages or depth > self.max_depth:
            return
            
        self.visited.add(url)
        logger.info(f"Crawling {url} (depth: {depth}, pages: {len(self.visited)}/{self.max_pages})")
        
        try:
            # Fetch the page
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to fetch {url}: {response.status}")
                        return
                        
                    content_type = response.headers.get('Content-Type', '')
                    if not content_type.startswith('text/html'):
                        logger.debug(f"Skipping non-HTML content: {url}")
                        return
                        
                    html = await response.text()
            
            # Parse the HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract text content
            text = self._extract_text(soup)
            
            # Check if the query is in the text
            if query.lower() in text.lower():
                # Extract relevant snippet
                snippet = self._extract_snippet(text, query)
                title = soup.title.string if soup.title else url
                
                # Add to results
                self.results.append({
                    "url": url,
                    "title": title,
                    "snippet": snippet,
                    "relevance": self._calculate_relevance(text, query)
                })
            
            # If we're not at max depth, extract links and crawl them
            if depth < self.max_depth:
                links = self._extract_links(soup, url)
                
                # Crawl each link
                tasks = []
                for link in links:
                    if link not in self.visited and len(self.visited) < self.max_pages:
                        tasks.append(self._crawl_page(link, query, depth + 1))
                
                if tasks:
                    await asyncio.gather(*tasks)
                    
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
    
    def _extract_text(self, soup) -> str:
        """Extract readable text from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space
        lines = (line.strip() for line in text.splitlines())
        
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _extract_snippet(self, text: str, query: str, context_chars: int = 100) -> str:
        """Extract a relevant snippet containing the query"""
        query_lower = query.lower()
        text_lower = text.lower()
        
        # Find position of query
        pos = text_lower.find(query_lower)
        if pos == -1:
            # If exact query not found, try to find partial matches
            words = query_lower.split()
            for word in words:
                if len(word) > 3:  # Only consider significant words
                    pos = text_lower.find(word)
                    if pos != -1:
                        break
            
            if pos == -1:
                # Still not found, return beginning of text
                return text[:200] + "..."
        
        # Extract context around the query
        start = max(0, pos - context_chars)
        end = min(len(text), pos + len(query) + context_chars)
        
        # Adjust to avoid cutting words
        if start > 0:
            while start > 0 and text[start] != ' ':
                start -= 1
        
        if end < len(text):
            while end < len(text) and text[end] != ' ':
                end += 1
        
        snippet = text[start:end].strip()
        
        # Add ellipsis if we're not at the beginning/end
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
            
        return snippet
    
    def _extract_links(self, soup, base_url: str) -> List[str]:
        """Extract links from HTML"""
        links = []
        base_domain = urlparse(base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Resolve relative URLs
            full_url = urljoin(base_url, href)
            
            # Parse the URL
            parsed = urlparse(full_url)
            
            # Only include links to the same domain
            if parsed.netloc == base_domain:
                # Exclude anchors, queries, etc.
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                
                # Remove trailing slash for consistency
                if clean_url.endswith('/'):
                    clean_url = clean_url[:-1]
                    
                links.append(clean_url)
        
        # Remove duplicates
        return list(set(links))
    
    def _calculate_relevance(self, text: str, query: str) -> float:
        """Calculate relevance score of text to query"""
        query_words = query.lower().split()
        text_lower = text.lower()
        
        # Count occurrences of query words
        word_counts = {}
        for word in query_words:
            if len(word) > 2:  # Ignore short words
                count = text_lower.count(word)
                word_counts[word] = count
        
        # Calculate average occurrences
        if not word_counts:
            return 0.0
            
        avg_count = sum(word_counts.values()) / len(word_counts)
        
        # Normalize to 0-1 range (max out at 10 occurrences)
        relevance = min(avg_count / 10.0, 1.0)
        
        # Boost if exact query is found
        if query.lower() in text_lower:
            relevance += 0.2
            
        # Boost if found in first 1000 chars (likely more important)
        if any(word in text_lower[:1000] for word in word_counts):
            relevance += 0.1
            
        return min(relevance, 1.0)
    
    async def _check_robots_txt(self, domain: str, url: str) -> bool:
        """Check if URL is allowed by robots.txt"""
        if domain in self.robots_cache:
            rules = self.robots_cache[domain]
        else:
            # Fetch robots.txt
            robots_url = f"https://{domain}/robots.txt"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(robots_url, timeout=5) as response:
                        if response.status == 200:
                            content = await response.text()
                            # Very simple robots.txt parser
                            rules = []
                            current_agent = None
                            for line in content.splitlines():
                                line = line.strip().lower()
                                if line.startswith('user-agent:'):
                                    agent = line[11:].strip()
                                    if agent == '*' or 'bot' in agent:
                                        current_agent = agent
                                elif current_agent and line.startswith('disallow:'):
                                    path = line[9:].strip()
                                    if path:
                                        rules.append(path)
                            
                            self.robots_cache[domain] = rules
                        else:
                            # If robots.txt not available, assume no rules
                            self.robots_cache[domain] = []
                            rules = []
            except Exception as e:
                logger.warning(f"Error fetching robots.txt for {domain}: {str(e)}")
                # Assume no rules if we can't fetch robots.txt
                self.robots_cache[domain] = []
                rules = []
        
        # Check if URL is disallowed
        path = urlparse(url).path
        for rule in rules:
            if path.startswith(rule):
                return False
                
        return True
    
    def _save_to_memory(self, query: str, results: List[Dict[str, Any]]) -> None:
        """Save crawling results to memory system"""
        if not self.memory_system:
            return
            
        try:
            # Sort results by relevance
            results = sorted(results, key=lambda x: x.get("relevance", 0), reverse=True)
            
            # Extract the main content
            content = "\n\n".join([
                f"URL: {result['url']}\nTitle: {result['title']}\n\n{result['snippet']}"
                for result in results[:5]  # Store top 5 results
            ])
            
            # Store in memory
            self.memory_system.add_memory(
                query=f"Web search: {query}",
                response=content,
                metadata={
                    "type": "web_search",
                    "urls": [result["url"] for result in results[:5]]
                }
            )
            
            logger.info(f"Saved web crawling results to memory for query: {query}")
        except Exception as e:
            logger.error(f"Error saving to memory: {str(e)}") 