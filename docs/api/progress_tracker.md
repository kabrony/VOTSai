# progress_tracker

## Classes

### Any

Special type indicating an unconstrained type.

    - Any is compatible with every type.
    - Any assumed to have all methods.
    - All values assumed to be instances of Any.

    Note that all the above statements are true from the point of view of
    static type checkers. At runtime, Any should not be used with instance
    checks.

### ProgressTracker

Track progress of long-running operations.

#### Methods

##### clean_old_operations

```python
clean_old_operations(self, max_age: float = 3600)
```

Remove old completed operations from memory.

##### complete_operation

```python
complete_operation(self, operation_id: str, result: Any = None)
```

Mark an operation as completed.

##### fail_operation

```python
fail_operation(self, operation_id: str, error: str)
```

Mark an operation as failed.

##### get_active_operations

```python
get_active_operations(self, client_id: Optional[str] = None)
```

Get all active operations, optionally filtered by client.

##### get_operation

```python
get_operation(self, operation_id: str)
```

Get the current state of an operation.

##### start_operation

```python
start_operation(self, operation_type: str, client_id: str = 'default')
```

Start tracking a new operation.

##### update_progress

```python
update_progress(self, operation_id: str, progress: float, message: str = None, step: str = None, eta: float = None)
```

Update progress of an operation.

