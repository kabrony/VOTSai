# models

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

### AsyncOpenAI

#### Methods

##### __init__

```python
__init__(self, api_key: 'str | None' = None, organization: 'str | None' = None, project: 'str | None' = None, base_url: 'str | httpx.URL | None' = None, websocket_base_url: 'str | httpx.URL | None' = None, timeout: 'Union[float, Timeout, None, NotGiven]' = NOT_GIVEN, max_retries: 'int' = 2, default_headers: 'Mapping[str, str] | None' = None, default_query: 'Mapping[str, object] | None' = None, http_client: 'httpx.AsyncClient | None' = None, _strict_response_validation: 'bool' = False)
```

Construct a new async openai client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `OPENAI_API_KEY`
        - `organization` from `OPENAI_ORG_ID`
        - `project` from `OPENAI_PROJECT_ID`

##### close

```python
close(self)
```

Close the underlying HTTPX client.

        The client will *not* be usable after this.

##### copy

```python
copy(self, api_key: 'str | None' = None, organization: 'str | None' = None, project: 'str | None' = None, websocket_base_url: 'str | httpx.URL | None' = None, base_url: 'str | httpx.URL | None' = None, timeout: 'float | Timeout | None | NotGiven' = NOT_GIVEN, http_client: 'httpx.AsyncClient | None' = None, max_retries: 'int | NotGiven' = NOT_GIVEN, default_headers: 'Mapping[str, str] | None' = None, set_default_headers: 'Mapping[str, str] | None' = None, default_query: 'Mapping[str, object] | None' = None, set_default_query: 'Mapping[str, object] | None' = None, _extra_kwargs: 'Mapping[str, Any]' = {})
```

Create a new client instance re-using the same options given to the current client with optional overriding.

##### delete

```python
delete(self, path: 'str', cast_to: 'Type[ResponseT]', body: 'Body | None' = None, options: 'RequestOptions' = {})
```

##### get

```python
get(self, path: 'str', cast_to: 'Type[ResponseT]', options: 'RequestOptions' = {}, stream: 'bool' = False, stream_cls: 'type[_AsyncStreamT] | None' = None)
```

##### get_api_list

```python
get_api_list(self, path: 'str', model: 'Type[_T]', page: 'Type[AsyncPageT]', body: 'Body | None' = None, options: 'RequestOptions' = {}, method: 'str' = 'get')
```

##### is_closed

```python
is_closed(self)
```

##### patch

```python
patch(self, path: 'str', cast_to: 'Type[ResponseT]', body: 'Body | None' = None, options: 'RequestOptions' = {})
```

##### platform_headers

```python
platform_headers(self)
```

##### post

```python
post(self, path: 'str', cast_to: 'Type[ResponseT]', body: 'Body | None' = None, files: 'RequestFiles | None' = None, options: 'RequestOptions' = {}, stream: 'bool' = False, stream_cls: 'type[_AsyncStreamT] | None' = None)
```

##### put

```python
put(self, path: 'str', cast_to: 'Type[ResponseT]', body: 'Body | None' = None, files: 'RequestFiles | None' = None, options: 'RequestOptions' = {})
```

##### request

```python
request(self, cast_to: 'Type[ResponseT]', options: 'FinalRequestOptions', stream: 'bool' = False, stream_cls: 'type[_AsyncStreamT] | None' = None, remaining_retries: 'Optional[int]' = None)
```

##### with_options

```python
with_options(self, api_key: 'str | None' = None, organization: 'str | None' = None, project: 'str | None' = None, websocket_base_url: 'str | httpx.URL | None' = None, base_url: 'str | httpx.URL | None' = None, timeout: 'float | Timeout | None | NotGiven' = NOT_GIVEN, http_client: 'httpx.AsyncClient | None' = None, max_retries: 'int | NotGiven' = NOT_GIVEN, default_headers: 'Mapping[str, str] | None' = None, set_default_headers: 'Mapping[str, str] | None' = None, default_query: 'Mapping[str, object] | None' = None, set_default_query: 'Mapping[str, object] | None' = None, _extra_kwargs: 'Mapping[str, Any]' = {})
```

Create a new client instance re-using the same options given to the current client with optional overriding.

### DeepSeekAPI

#### Methods

##### __init__

```python
__init__(self)
```

##### fetch_web_context

```python
fetch_web_context(self, query: str, timeout: int, depth: int = 1)
```

##### query

```python
query(self, query: str, timeout: int, memory_context: str, web_context: str = '', temperature: float = 0.7)
```

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

### LocalDeepSeek

#### Methods

##### __init__

```python
__init__(self)
```

##### fetch_web_context

```python
fetch_web_context(self, query: str, timeout: int, depth: int = 1)
```

##### query

```python
query(self, query: str, timeout: int, memory_context: str, web_context: str = '', temperature: float = 0.7)
```

##### query_sync

```python
query_sync(self, query: str, memory_context: str, web_context: str = '', temperature: float = 0.7)
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

### PerplexityAPI

#### Methods

##### __init__

```python
__init__(self)
```

##### fetch_web_context

```python
fetch_web_context(self, query: str, timeout: int, depth: int = 1)
```

##### query

```python
query(self, query: str, timeout: int, memory_context: str, web_context: str = '', temperature: float = 0.7)
```

### stop_after_attempt

Stop when the previous attempt >= max_attempt.

#### Methods

##### __init__

```python
__init__(self, max_attempt_number: int)
```

### wait_exponential

Wait strategy that applies exponential backoff.

    It allows for a customized multiplier and an ability to restrict the
    upper and lower limits to some maximum and minimum value.

    The intervals are fixed (i.e. there is no jitter), so this strategy is
    suitable for balancing retries against latency when a required resource is
    unavailable for an unknown duration, but *not* suitable for resolving
    contention between multiple processes for a shared resource. Use
    wait_random_exponential for the latter case.

#### Methods

##### __init__

```python
__init__(self, multiplier: Union[int, float] = 1, max: Union[int, float, datetime.timedelta] = 4.611686018427388e+18, exp_base: Union[int, float] = 2, min: Union[int, float, datetime.timedelta] = 0)
```

## Functions

### count_tokens

```python
count_tokens(text: str, model_name: str)
```

### retry

```python
retry(*dargs: Any, **dkw: Any)
```

Wrap a function with a new `Retrying` object.

    :param dargs: positional arguments passed to Retrying object
    :param dkw: keyword arguments passed to the Retrying object

