# token_manager

## Classes

### TokenManager

Efficiently manage and count tokens for various models.

#### Methods

##### count_tokens

```python
count_tokens(text: str, model_name: str)
```

Count tokens in text for a specific model with caching.

##### estimate_cost

```python
estimate_cost(input_tokens: int, output_tokens: int, model_name: str)
```

Estimate the cost of a query in USD.

##### split_into_chunks

```python
split_into_chunks(text: str, chunk_size: int, model_name: str, overlap: int = 0)
```

Split text into chunks of roughly chunk_size tokens with optional overlap.

##### truncate_to_tokens

```python
truncate_to_tokens(text: str, max_tokens: int, model_name: str)
```

Truncate text to fit within max_tokens.

## Functions

### lru_cache

```python
lru_cache(maxsize=128, typed=False)
```

Least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    If *typed* is True, arguments of different types will be cached separately.
    For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits, misses, maxsize, currsize)
    with f.cache_info().  Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.

    See:  https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)

