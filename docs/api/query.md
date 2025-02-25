# query

## Classes

### AIModel

#### Methods

##### __init__

```python
__init__(self, name: str)
```

##### fetch_web_context

```python
fetch_web_context(self, query: str, timeout: int, depth: int = 1)
```

##### query

```python
query(self, query: str, timeout: int, memory_context: str, web_context: str = '', temperature: float = 0.7)
```

### Any

Special type indicating an unconstrained type.

    - Any is compatible with every type.
    - Any assumed to have all methods.
    - All values assumed to be instances of Any.

    Note that all the above statements are true from the point of view of
    static type checkers. At runtime, Any should not be used with instance
    checks.

## Functions

### crawl_url

```python
crawl_url(url: str, timeout: int)
```

### format_response

```python
format_response(query: str, result: Dict[str, Any], share_format: str = 'Text')
```

### get_relevant_memory

```python
get_relevant_memory(conn: sqlite3.Connection, query: str, limit: int = 3)
```

### handle_crawl_query

```python
handle_crawl_query(query: str, timeout: int, memory_context: str, start_time: float, model: core.models.AIModel, web_priority: bool, temperature: float, share_format: str)
```

### handle_general_query

```python
handle_general_query(query: str, timeout: int, memory_context: str, start_time: float, model: core.models.AIModel, web_priority: bool, temperature: float, share_format: str)
```

### handle_recall_query

```python
handle_recall_query(query: str, conn: sqlite3.Connection, start_time: float, share_format: str)
```

### orchestrate_query

```python
orchestrate_query(query: str, timeout: int, short_term_memory: Deque, conn: sqlite3.Connection, model: core.models.AIModel, web_priority: bool = True, temperature: float = 0.7, share_format: str = 'Text')
```

### update_memory

```python
update_memory(conn: sqlite3.Connection, query: str, result: Dict[str, Any], short_term_memory: Deque)
```

