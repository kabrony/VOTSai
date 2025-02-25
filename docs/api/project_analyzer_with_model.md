# project_analyzer_with_model

## Classes

### IntentClassifier

#### Methods

##### __init__

```python
__init__(self)
```

##### predict

```python
predict(self, query: str)
```

### ModelFactory

#### Methods

##### create_model

```python
create_model(self, model_name: str)
```

##### select_model

```python
select_model(self, query: str, user_selected: str, web_priority: bool, classifier: core.classifier.IntentClassifier)
```

### datetime

datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints.

## Functions

### analyze_file

```python
analyze_file(model, file_path, conn)
```

Analyze a single file asynchronously.

### analyze_project

```python
analyze_project(directory='.', max_concurrent=5)
```

Analyze key Python files concurrently with controlled concurrency.

### basic_code_analysis

```python
basic_code_analysis(file_path)
```

Perform basic static analysis on a Python file.

### get_memory_usage

```python
get_memory_usage()
```

Get current process memory usage in MB.

### get_model_suggestions

```python
get_model_suggestions(model, file_path, code, basic_findings, conn, timeout=120)
```

Use the DeepSeek model with a timeout and retry.

### get_relevant_memory

```python
get_relevant_memory(conn: sqlite3.Connection, query: str, limit: int = 3)
```

### load_env

```python
load_env()
```

Load environment variables from .env file.

