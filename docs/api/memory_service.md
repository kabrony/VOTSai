# memory_service

## Classes

### Any

Special type indicating an unconstrained type.

    - Any is compatible with every type.
    - Any assumed to have all methods.
    - All values assumed to be instances of Any.

    Note that all the above statements are true from the point of view of
    static type checkers. At runtime, Any should not be used with instance
    checks.

### MemoryService

Service for memory-related database operations.

#### Methods

##### __init__

```python
__init__(self, db_path: str)
```

##### add_memory

```python
add_memory(self, query: str, answer: str, model_used: str = '', tags: List[str] = None)
```

Add a new memory to the database.

##### clear_memories

```python
clear_memories(self)
```

Clear all memories from the database.

##### close

```python
close(self)
```

Close database connection.

##### get_memories_by_date

```python
get_memories_by_date(self, start_date: str, end_date: str)
```

Get memories within a date range.

##### get_relevant_memories

```python
get_relevant_memories(self, query: str, limit: int = 3)
```

Get memories relevant to a query.

##### update_memory_from_short_term

```python
update_memory_from_short_term(self, short_term_memory: Deque)
```

Update long-term memory from short-term memory.

### datetime

datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints.

