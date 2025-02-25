# doc_generator

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

### document_class

```python
document_class(f, name: str, cls: type)
```

Generate documentation for a class.
    
    Args:
        f: File handle to write to
        name: Name of the class
        cls: Class object to document

#### Parameters

- **f**: File handle to write to
- **name**: Name of the class
- **cls**: Class object to document

### document_function

```python
document_function(f, name: str, func: Callable, indent: bool = False)
```

Generate documentation for a function.
    
    Args:
        f: File handle to write to
        name: Name of the function
        func: Function object to document
        indent: Whether to indent the documentation

#### Parameters

- **f**: File handle to write to
- **name**: Name of the function
- **func**: Function object to document
- **indent**: Whether to indent the documentation

### document_method

```python
document_method(f, name: str, method: Callable)
```

Generate documentation for a method.
    
    Args:
        f: File handle to write to
        name: Name of the method
        method: Method object to document

#### Parameters

- **f**: File handle to write to
- **name**: Name of the method
- **method**: Method object to document

### document_module

```python
document_module(module_path: str, output_dir: str, skip_import_errors: bool = False, verbose: bool = False)
```

Generate markdown documentation for a Python module.
    
    Args:
        module_path: Path to the Python module file
        output_dir: Directory to write the documentation to
        skip_import_errors: If True, continue execution despite import errors
        verbose: If True, print detailed error messages
        
    Returns:
        Tuple of (success, error_message)

#### Parameters

- **module_path**: Path to the Python module file
- **output_dir**: Directory to write the documentation to
- **skip_import_errors**: If True, continue execution despite import errors
- **verbose**: If True, print detailed error messages

#### Returns

Tuple of (success, error_message)

### generate_project_documentation

```python
generate_project_documentation(project_dir: str, output_dir: str, exclude_patterns: List[str] = None, skip_import_errors: bool = False, dry_run: bool = False, max_depth: int = None, verbose: bool = False, include_standard_lib: bool = False, rate_limit: float = 0.0)
```

Generate documentation for an entire project.
    
    Args:
        project_dir: Root directory of the project
        output_dir: Directory to write documentation to
        exclude_patterns: List of glob patterns to exclude
        skip_import_errors: If True, continue execution despite import errors
        dry_run: If True, only check for errors without generating docs
        max_depth: Maximum directory depth to traverse
        verbose: If True, print detailed output
        include_standard_lib: If True, document modules from standard library
        rate_limit: Seconds to wait between processing files (to prevent system overload)
        
    Returns:
        Dictionary with successful and failed module documentation attempts

#### Parameters

- **project_dir**: Root directory of the project
- **output_dir**: Directory to write documentation to
- **exclude_patterns**: List of glob patterns to exclude
- **skip_import_errors**: If True, continue execution despite import errors
- **dry_run**: If True, only check for errors without generating docs
- **max_depth**: Maximum directory depth to traverse
- **verbose**: If True, print detailed output
- **include_standard_lib**: If True, document modules from standard library
- **rate_limit**: Seconds to wait between processing files (to prevent system overload)

#### Returns

Dictionary with successful and failed module documentation attempts

