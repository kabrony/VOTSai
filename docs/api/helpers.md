# helpers

## Classes

### Any

Special type indicating an unconstrained type.

    - Any is compatible with every type.
    - Any assumed to have all methods.
    - All values assumed to be instances of Any.

    Note that all the above statements are true from the point of view of
    static type checkers. At runtime, Any should not be used with instance
    checks.

## Functions

### count_tokens

```python
count_tokens(text: str, model_name: str)
```

### format_response

```python
format_response(query: str, result: Dict[str, Any], share_format: str = 'Text')
```

