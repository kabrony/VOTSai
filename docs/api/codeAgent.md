# codeAgent

## Classes

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

## Functions

### analyze_code

```python
analyze_code(code: str)
```

