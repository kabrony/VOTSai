# rate_limiter

## Classes

### RateLimiter

Rate limiting utility to prevent API abuse.

#### Methods

##### check_rate_limit

```python
check_rate_limit(self, client_id: str)
```

Check if client is within rate limits.

##### get_usage_stats

```python
get_usage_stats(self, client_id: str)
```

Get usage statistics for a client.

##### record_request

```python
record_request(self, client_id: str, input_tokens: int = 0, output_tokens: int = 0)
```

Record a request for rate limiting purposes.

### defaultdict

defaultdict(default_factory=None, /, [...]) --> dict with default factory

The default factory is called without arguments to produce
a new value when a key is not present, in __getitem__ only.
A defaultdict compares equal to a dict with the same items.
All remaining arguments are treated the same as if they were
passed to the dict constructor, including keyword arguments.

