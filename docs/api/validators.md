# validators

## Classes

### Any

Special type indicating an unconstrained type.

    - Any is compatible with every type.
    - Any assumed to have all methods.
    - All values assumed to be instances of Any.

    Note that all the above statements are true from the point of view of
    static type checkers. At runtime, Any should not be used with instance
    checks.

### Validator

Input validation utility for VOTSai.

#### Methods

##### sanitize_output

```python
sanitize_output(output: str)
```

Sanitize model output.

##### sanitize_query

```python
sanitize_query(query: str)
```

Sanitize user query for safe storage and display.

##### validate_code

```python
validate_code(code: str)
```

Validate user-submitted code.

##### validate_file_path

```python
validate_file_path(path: str)
```

Validate file path to prevent directory traversal.

##### validate_model_params

```python
validate_model_params(params: Dict[str, Any])
```

Validate model parameters for safety and correctness.

##### validate_query

```python
validate_query(query: str)
```

Validate user query input.

##### validate_url

```python
validate_url(url: str)
```

Validate URL for web crawling.

