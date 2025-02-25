# web

## Classes

### AsyncWebCrawler

Asynchronous web crawler with flexible caching capabilities.

    There are two ways to use the crawler:

    1. Using context manager (recommended for simple cases):
        ```python
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url="https://example.com")
        ```

    2. Using explicit lifecycle management (recommended for long-running applications):
        ```python
        crawler = AsyncWebCrawler()
        await crawler.start()

        # Use the crawler multiple times
        result1 = await crawler.arun(url="https://example.com")
        result2 = await crawler.arun(url="https://another.com")

        await crawler.close()
        ```

    Migration Guide:
    Old way (deprecated):
        crawler = AsyncWebCrawler(always_by_pass_cache=True, browser_type="chromium", headless=True)

    New way (recommended):
        browser_config = BrowserConfig(browser_type="chromium", headless=True)
        crawler = AsyncWebCrawler(config=browser_config)


    Attributes:
        browser_config (BrowserConfig): Configuration object for browser settings.
        crawler_strategy (AsyncCrawlerStrategy): Strategy for crawling web pages.
        logger (AsyncLogger): Logger instance for recording events and errors.
        always_bypass_cache (bool): Whether to always bypass cache.
        crawl4ai_folder (str): Directory for storing cache.
        base_directory (str): Base directory for storing cache.
        ready (bool): Whether the crawler is ready for use.

        Methods:
            start(): Start the crawler explicitly without using context manager.
            close(): Close the crawler explicitly without using context manager.
            arun(): Run the crawler for a single source: URL (web, local file, or raw HTML).
            awarmup(): Perform warmup sequence.
            arun_many(): Run the crawler for multiple sources.
            aprocess_html(): Process HTML content.

    Typical Usage:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url="https://example.com")
            print(result.markdown)

        Using configuration:
        browser_config = BrowserConfig(browser_type="chromium", headless=True)
        async with AsyncWebCrawler(config=browser_config) as crawler:
            crawler_config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS
            )
            result = await crawler.arun(url="https://example.com", config=crawler_config)
            print(result.markdown)

#### Methods

##### __init__

```python
__init__(self, crawler_strategy: Optional[crawl4ai.async_crawler_strategy.AsyncCrawlerStrategy] = None, config: Optional[crawl4ai.async_configs.BrowserConfig] = None, always_bypass_cache: bool = False, always_by_pass_cache: Optional[bool] = None, base_directory: str = '/home/vots', thread_safe: bool = False, **kwargs)
```

Initialize the AsyncWebCrawler.

        Args:
            crawler_strategy: Strategy for crawling web pages. If None, will create AsyncPlaywrightCrawlerStrategy
            config: Configuration object for browser settings. If None, will be created from kwargs
            always_bypass_cache: Whether to always bypass cache (new parameter)
            always_by_pass_cache: Deprecated, use always_bypass_cache instead
            base_directory: Base directory for storing cache
            thread_safe: Whether to use thread-safe operations
            **kwargs: Additional arguments for backwards compatibility

###### Parameters

- **crawler_strategy**: Strategy for crawling web pages. If None, will create AsyncPlaywrightCrawlerStrategy
- **config**: Configuration object for browser settings. If None, will be created from kwargs
- **always_bypass_cache**: Whether to always bypass cache (new parameter)
- **always_by_pass_cache**: Deprecated, use always_bypass_cache instead
- **base_directory**: Base directory for storing cache
- **thread_safe**: Whether to use thread-safe operations
            **kwargs: Additional arguments for backwards compatibility

##### aclear_cache

```python
aclear_cache(self)
```

Clear the cache database.

##### aflush_cache

```python
aflush_cache(self)
```

Flush the cache database.

##### aget_cache_size

```python
aget_cache_size(self)
```

Get the total number of cached items.

##### aprocess_html

```python
aprocess_html(self, url: str, html: str, extracted_content: str, config: crawl4ai.async_configs.CrawlerRunConfig, screenshot: str, pdf_data: str, verbose: bool, **kwargs)
```

Process HTML content using the provided configuration.

        Args:
            url: The URL being processed
            html: Raw HTML content
            extracted_content: Previously extracted content (if any)
            config: Configuration object controlling processing behavior
            screenshot: Screenshot data (if any)
            pdf_data: PDF data (if any)
            verbose: Whether to enable verbose logging
            **kwargs: Additional parameters for backwards compatibility

        Returns:
            CrawlResult: Processed result containing extracted and formatted content

###### Parameters

- **url**: The URL being processed
- **html**: Raw HTML content
- **extracted_content**: Previously extracted content (if any)
- **config**: Configuration object controlling processing behavior
- **screenshot**: Screenshot data (if any)
- **pdf_data**: PDF data (if any)
- **verbose**: Whether to enable verbose logging
            **kwargs: Additional parameters for backwards compatibility

###### Returns



##### arun

```python
arun(self, url: str, config: Optional[crawl4ai.async_configs.CrawlerRunConfig] = None, word_count_threshold=1, extraction_strategy: crawl4ai.extraction_strategy.ExtractionStrategy = None, chunking_strategy: crawl4ai.chunking_strategy.ChunkingStrategy = <crawl4ai.chunking_strategy.RegexChunking object at 0x7f1700e2fad0>, content_filter: crawl4ai.content_filter_strategy.RelevantContentFilter = None, cache_mode: Optional[crawl4ai.cache_context.CacheMode] = None, bypass_cache: bool = False, disable_cache: bool = False, no_cache_read: bool = False, no_cache_write: bool = False, css_selector: str = None, screenshot: bool = False, pdf: bool = False, user_agent: str = None, verbose=True, **kwargs)
```

Runs the crawler for a single source: URL (web, local file, or raw HTML).

        Migration Guide:
        Old way (deprecated):
            result = await crawler.arun(
                url="https://example.com",
                word_count_threshold=200,
                screenshot=True,
                ...
            )

        New way (recommended):
            config = CrawlerRunConfig(
                word_count_threshold=200,
                screenshot=True,
                ...
            )
            result = await crawler.arun(url="https://example.com", crawler_config=config)

        Args:
            url: The URL to crawl (http://, https://, file://, or raw:)
            crawler_config: Configuration object controlling crawl behavior
            [other parameters maintained for backwards compatibility]

        Returns:
            CrawlResult: The result of crawling and processing

###### Parameters

- **url**: The URL to crawl (http://, https://, file://, or raw:)

###### Returns



##### arun_many

```python
arun_many(self, urls: List[str], config: Optional[crawl4ai.async_configs.CrawlerRunConfig] = None, dispatcher: Optional[crawl4ai.async_dispatcher.BaseDispatcher] = None, word_count_threshold=1, extraction_strategy: crawl4ai.extraction_strategy.ExtractionStrategy = None, chunking_strategy: crawl4ai.chunking_strategy.ChunkingStrategy = <crawl4ai.chunking_strategy.RegexChunking object at 0x7f1700e2fb30>, content_filter: crawl4ai.content_filter_strategy.RelevantContentFilter = None, cache_mode: Optional[crawl4ai.cache_context.CacheMode] = None, bypass_cache: bool = False, css_selector: str = None, screenshot: bool = False, pdf: bool = False, user_agent: str = None, verbose=True, **kwargs)
```

Runs the crawler for multiple URLs concurrently using a configurable dispatcher strategy.

        Args:
        urls: List of URLs to crawl
        config: Configuration object controlling crawl behavior for all URLs
        dispatcher: The dispatcher strategy instance to use. Defaults to MemoryAdaptiveDispatcher
        [other parameters maintained for backwards compatibility]

        Returns:
        Union[List[CrawlResult], AsyncGenerator[CrawlResult, None]]:
            Either a list of all results or an async generator yielding results

        Examples:

        # Batch processing (default)
        results = await crawler.arun_many(
            urls=["https://example1.com", "https://example2.com"],
            config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
        )
        for result in results:
            print(f"Processed {result.url}: {len(result.markdown)} chars")

        # Streaming results
        async for result in await crawler.arun_many(
            urls=["https://example1.com", "https://example2.com"],
            config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=True),
        ):
            print(f"Processed {result.url}: {len(result.markdown)} chars")

###### Parameters

- **urls**: List of URLs to crawl
- **config**: Configuration object controlling crawl behavior for all URLs
- **dispatcher**: The dispatcher strategy instance to use. Defaults to MemoryAdaptiveDispatcher
        [other parameters maintained for backwards compatibility]

###### Returns

Union[List[CrawlResult], AsyncGenerator[CrawlResult, None]]:
            Either a list of all results or an async generator yielding results

##### awarmup

```python
awarmup(self)
```

Initialize the crawler with warm-up sequence.

        This method:
        1. Logs initialization info
        2. Sets up browser configuration
        3. Marks the crawler as ready

##### close

```python
close(self)
```

Close the crawler explicitly without using context manager.
        This should be called when you're done with the crawler if you used start().

        This method will:
        1. Clean up browser resources
        2. Close any open pages and contexts

##### nullcontext

```python
nullcontext(self)
```

异步空上下文管理器

##### start

```python
start(self)
```

Start the crawler explicitly without using context manager.
        This is equivalent to using 'async with' but gives more control over the lifecycle.

        This method will:
        1. Initialize the browser and context
        2. Perform warmup sequence
        3. Return the crawler instance for method chaining

        Returns:
            AsyncWebCrawler: The initialized crawler instance

###### Returns



## Functions

### crawl_url

```python
crawl_url(url: str, timeout: int)
```

