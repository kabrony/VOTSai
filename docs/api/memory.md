# memory

## Classes

### Any

Special type indicating an unconstrained type.

    - Any is compatible with every type.
    - Any assumed to have all methods.
    - All values assumed to be instances of Any.

    Note that all the above statements are true from the point of view of
    static type checkers. At runtime, Any should not be used with instance
    checks.

### datetime

datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints.

### deque

deque([iterable[, maxlen]]) --> deque object

A list-like sequence optimized for data accesses near its endpoints.

## Functions

### get_relevant_memory

```python
get_relevant_memory(conn: sqlite3.Connection, query: str, limit: int = 3)
```

### init_memory_db

```python
init_memory_db(db_path: str = 'vots_agi_memory.db')
```

### update_memory

```python
update_memory(conn: sqlite3.Connection, query: str, result: Dict[str, Any], short_term_memory: Deque)
```

