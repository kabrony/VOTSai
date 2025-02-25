# analyze_project

## Classes

### OllamaLLM

OllamaLLM large language models.

    Example:
        .. code-block:: python

            from langchain_ollama import OllamaLLM

            model = OllamaLLM(model="llama3")
            model.invoke("Come up with 10 names for a song about parrots")

#### Methods

##### __init__

```python
__init__(self, *args: Any, **kwargs: Any)
```

##### abatch

```python
abatch(self, inputs: 'list[LanguageModelInput]', config: 'Optional[Union[RunnableConfig, list[RunnableConfig]]]' = None, return_exceptions: 'bool' = False, **kwargs: 'Any')
```

##### abatch_as_completed

```python
abatch_as_completed(self, inputs: 'Sequence[Input]', config: 'Optional[Union[RunnableConfig, Sequence[RunnableConfig]]]' = None, return_exceptions: 'bool' = False, **kwargs: 'Optional[Any]')
```

Run ainvoke in parallel on a list of inputs,
        yielding results as they complete.

        Args:
            inputs: A list of inputs to the Runnable.
            config: A config to use when invoking the Runnable.
               The config supports standard keys like 'tags', 'metadata' for tracing
               purposes, 'max_concurrency' for controlling how much work to do
               in parallel, and other keys. Please refer to the RunnableConfig
               for more details. Defaults to None. Defaults to None.
            return_exceptions: Whether to return exceptions instead of raising them.
                Defaults to False.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            A tuple of the index of the input and the output from the Runnable.

###### Parameters

- **inputs**: A list of inputs to the Runnable.
- **config**: A config to use when invoking the Runnable.
               The config supports standard keys like 'tags', 'metadata' for tracing
               purposes, 'max_concurrency' for controlling how much work to do
               in parallel, and other keys. Please refer to the RunnableConfig
               for more details. Defaults to None. Defaults to None.
- **return_exceptions**: Whether to return exceptions instead of raising them.
                Defaults to False.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### agenerate

```python
agenerate(self, prompts: 'list[str]', stop: 'Optional[list[str]]' = None, callbacks: 'Optional[Union[Callbacks, list[Callbacks]]]' = None, tags: 'Optional[Union[list[str], list[list[str]]]]' = None, metadata: 'Optional[Union[dict[str, Any], list[dict[str, Any]]]]' = None, run_name: 'Optional[Union[str, list[str]]]' = None, run_id: 'Optional[Union[uuid.UUID, list[Optional[uuid.UUID]]]]' = None, **kwargs: 'Any')
```

Asynchronously pass a sequence of prompts to a model and return generations.

        This method should make use of batched calls for models that expose a batched
        API.

        Use this method when you want to:
            1. take advantage of batched calls,
            2. need more output from the model than just the top generated value,
            3. are building chains that are agnostic to the underlying language model
                type (e.g., pure text completion models vs chat models).

        Args:
            prompts: List of string prompts.
            stop: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of these substrings.
            callbacks: Callbacks to pass through. Used for executing additional
                functionality, such as logging or streaming, throughout generation.
            tags: List of tags to associate with each prompt. If provided, the length
                of the list must match the length of the prompts list.
            metadata: List of metadata dictionaries to associate with each prompt. If
                provided, the length of the list must match the length of the prompts
                list.
            run_name: List of run names to associate with each prompt. If provided, the
                length of the list must match the length of the prompts list.
            run_id: List of run IDs to associate with each prompt. If provided, the
                length of the list must match the length of the prompts list.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            An LLMResult, which contains a list of candidate Generations for each input
                prompt and additional model provider-specific output.

###### Parameters

- **prompts**: List of string prompts.
- **stop**: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of these substrings.
- **callbacks**: Callbacks to pass through. Used for executing additional
                functionality, such as logging or streaming, throughout generation.
- **tags**: List of tags to associate with each prompt. If provided, the length
                of the list must match the length of the prompts list.
- **metadata**: List of metadata dictionaries to associate with each prompt. If
                provided, the length of the list must match the length of the prompts
                list.
- **run_name**: List of run names to associate with each prompt. If provided, the
                length of the list must match the length of the prompts list.
- **run_id**: List of run IDs to associate with each prompt. If provided, the
                length of the list must match the length of the prompts list.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

###### Returns

An LLMResult, which contains a list of candidate Generations for each input
                prompt and additional model provider-specific output.

##### agenerate_prompt

```python
agenerate_prompt(self, prompts: 'list[PromptValue]', stop: 'Optional[list[str]]' = None, callbacks: 'Optional[Union[Callbacks, list[Callbacks]]]' = None, **kwargs: 'Any')
```

##### ainvoke

```python
ainvoke(self, input: 'LanguageModelInput', config: 'Optional[RunnableConfig]' = None, stop: 'Optional[list[str]]' = None, **kwargs: 'Any')
```

##### apredict

```python
apredict(self, text: 'str', stop: 'Optional[Sequence[str]]' = None, **kwargs: 'Any')
```

.. deprecated:: 0.1.7 Use :meth:`~ainvoke` instead. It will not be removed until langchain-core==1.0.

##### apredict_messages

```python
apredict_messages(self, messages: 'list[BaseMessage]', stop: 'Optional[Sequence[str]]' = None, **kwargs: 'Any')
```

.. deprecated:: 0.1.7 Use :meth:`~ainvoke` instead. It will not be removed until langchain-core==1.0.

##### as_tool

```python
as_tool(self, args_schema: 'Optional[type[BaseModel]]' = None, name: 'Optional[str]' = None, description: 'Optional[str]' = None, arg_types: 'Optional[dict[str, type]]' = None)
```

.. beta::
   This API is in beta and may change in the future.

Create a BaseTool from a Runnable.

``as_tool`` will instantiate a BaseTool with a name, description, and
``args_schema`` from a Runnable. Where possible, schemas are inferred
from ``runnable.get_input_schema``. Alternatively (e.g., if the
Runnable takes a dict as input and the specific dict keys are not typed),
the schema can be specified directly with ``args_schema``. You can also
pass ``arg_types`` to just specify the required arguments and their types.

Args:
    args_schema: The schema for the tool. Defaults to None.
    name: The name of the tool. Defaults to None.
    description: The description of the tool. Defaults to None.
    arg_types: A dictionary of argument names to types. Defaults to None.

Returns:
    A BaseTool instance.

Typed dict input:

.. code-block:: python

    from typing import List
    from typing_extensions import TypedDict
    from langchain_core.runnables import RunnableLambda

    class Args(TypedDict):
        a: int
        b: List[int]

    def f(x: Args) -> str:
        return str(x["a"] * max(x["b"]))

    runnable = RunnableLambda(f)
    as_tool = runnable.as_tool()
    as_tool.invoke({"a": 3, "b": [1, 2]})

``dict`` input, specifying schema via ``args_schema``:

.. code-block:: python

    from typing import Any, Dict, List
    from pydantic import BaseModel, Field
    from langchain_core.runnables import RunnableLambda

    def f(x: Dict[str, Any]) -> str:
        return str(x["a"] * max(x["b"]))

    class FSchema(BaseModel):
        """Apply a function to an integer and list of integers."""

        a: int = Field(..., description="Integer")
        b: List[int] = Field(..., description="List of ints")

    runnable = RunnableLambda(f)
    as_tool = runnable.as_tool(FSchema)
    as_tool.invoke({"a": 3, "b": [1, 2]})

``dict`` input, specifying schema via ``arg_types``:

.. code-block:: python

    from typing import Any, Dict, List
    from langchain_core.runnables import RunnableLambda

    def f(x: Dict[str, Any]) -> str:
        return str(x["a"] * max(x["b"]))

    runnable = RunnableLambda(f)
    as_tool = runnable.as_tool(arg_types={"a": int, "b": List[int]})
    as_tool.invoke({"a": 3, "b": [1, 2]})

String input:

.. code-block:: python

    from langchain_core.runnables import RunnableLambda

    def f(x: str) -> str:
        return x + "a"

    def g(x: str) -> str:
        return x + "z"

    runnable = RunnableLambda(f) | g
    as_tool = runnable.as_tool()
    as_tool.invoke("b")

.. versionadded:: 0.2.14

###### Parameters

- **args_schema**: The schema for the tool. Defaults to None.
- **name**: The name of the tool. Defaults to None.
- **description**: The description of the tool. Defaults to None.
- **arg_types**: A dictionary of argument names to types. Defaults to None.

###### Returns

A BaseTool instance.

Typed dict input:

.. code-block:: python

    from typing import List
    from typing_extensions import TypedDict
    from langchain_core.runnables import RunnableLambda

    class Args(TypedDict):

##### assign

```python
assign(self, **kwargs: 'Union[Runnable[dict[str, Any], Any], Callable[[dict[str, Any]], Any], Mapping[str, Union[Runnable[dict[str, Any], Any], Callable[[dict[str, Any]], Any]]]]')
```

Assigns new fields to the dict output of this Runnable.
        Returns a new Runnable.

        .. code-block:: python

            from langchain_community.llms.fake import FakeStreamingListLLM
            from langchain_core.output_parsers import StrOutputParser
            from langchain_core.prompts import SystemMessagePromptTemplate
            from langchain_core.runnables import Runnable
            from operator import itemgetter

            prompt = (
                SystemMessagePromptTemplate.from_template("You are a nice assistant.")
                + "{question}"
            )
            llm = FakeStreamingListLLM(responses=["foo-lish"])

            chain: Runnable = prompt | llm | {"str": StrOutputParser()}

            chain_with_assign = chain.assign(hello=itemgetter("str") | llm)

            print(chain_with_assign.input_schema.model_json_schema())
            # {'title': 'PromptInput', 'type': 'object', 'properties':
            {'question': {'title': 'Question', 'type': 'string'}}}
            print(chain_with_assign.output_schema.model_json_schema())
            # {'title': 'RunnableSequenceOutput', 'type': 'object', 'properties':
            {'str': {'title': 'Str',
            'type': 'string'}, 'hello': {'title': 'Hello', 'type': 'string'}}}

##### astream

```python
astream(self, input: 'LanguageModelInput', config: 'Optional[RunnableConfig]' = None, stop: 'Optional[list[str]]' = None, **kwargs: 'Any')
```

##### astream_events

```python
astream_events(self, input: 'Any', config: 'Optional[RunnableConfig]' = None, version: "Literal['v1', 'v2']", include_names: 'Optional[Sequence[str]]' = None, include_types: 'Optional[Sequence[str]]' = None, include_tags: 'Optional[Sequence[str]]' = None, exclude_names: 'Optional[Sequence[str]]' = None, exclude_types: 'Optional[Sequence[str]]' = None, exclude_tags: 'Optional[Sequence[str]]' = None, **kwargs: 'Any')
```

Generate a stream of events.

        Use to create an iterator over StreamEvents that provide real-time information
        about the progress of the Runnable, including StreamEvents from intermediate
        results.

        A StreamEvent is a dictionary with the following schema:

        - ``event``: **str** - Event names are of the
            format: on_[runnable_type]_(start|stream|end).
        - ``name``: **str** - The name of the Runnable that generated the event.
        - ``run_id``: **str** - randomly generated ID associated with the given execution of
            the Runnable that emitted the event.
            A child Runnable that gets invoked as part of the execution of a
            parent Runnable is assigned its own unique ID.
        - ``parent_ids``: **List[str]** - The IDs of the parent runnables that
            generated the event. The root Runnable will have an empty list.
            The order of the parent IDs is from the root to the immediate parent.
            Only available for v2 version of the API. The v1 version of the API
            will return an empty list.
        - ``tags``: **Optional[List[str]]** - The tags of the Runnable that generated
            the event.
        - ``metadata``: **Optional[Dict[str, Any]]** - The metadata of the Runnable
            that generated the event.
        - ``data``: **Dict[str, Any]**


        Below is a table that illustrates some events that might be emitted by various
        chains. Metadata fields have been omitted from the table for brevity.
        Chain definitions have been included after the table.

        **ATTENTION** This reference table is for the V2 version of the schema.

        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | event                | name             | chunk                           | input                                         | output                                          |
        +======================+==================+=================================+===============================================+=================================================+
        | on_chat_model_start  | [model name]     |                                 | {"messages": [[SystemMessage, HumanMessage]]} |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chat_model_stream | [model name]     | AIMessageChunk(content="hello") |                                               |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chat_model_end    | [model name]     |                                 | {"messages": [[SystemMessage, HumanMessage]]} | AIMessageChunk(content="hello world")           |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_llm_start         | [model name]     |                                 | {'input': 'hello'}                            |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_llm_stream        | [model name]     | 'Hello'                         |                                               |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_llm_end           | [model name]     |                                 | 'Hello human!'                                |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chain_start       | format_docs      |                                 |                                               |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chain_stream      | format_docs      | "hello world!, goodbye world!"  |                                               |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chain_end         | format_docs      |                                 | [Document(...)]                               | "hello world!, goodbye world!"                  |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_tool_start        | some_tool        |                                 | {"x": 1, "y": "2"}                            |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_tool_end          | some_tool        |                                 |                                               | {"x": 1, "y": "2"}                              |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_retriever_start   | [retriever name] |                                 | {"query": "hello"}                            |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_retriever_end     | [retriever name] |                                 | {"query": "hello"}                            | [Document(...), ..]                             |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_prompt_start      | [template_name]  |                                 | {"question": "hello"}                         |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_prompt_end        | [template_name]  |                                 | {"question": "hello"}                         | ChatPromptValue(messages: [SystemMessage, ...]) |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+

        In addition to the standard events, users can also dispatch custom events (see example below).

        Custom events will be only be surfaced with in the `v2` version of the API!

        A custom event has following format:

        +-----------+------+-----------------------------------------------------------------------------------------------------------+
        | Attribute | Type | Description                                                                                               |
        +===========+======+===========================================================================================================+
        | name      | str  | A user defined name for the event.                                                                        |
        +-----------+------+-----------------------------------------------------------------------------------------------------------+
        | data      | Any  | The data associated with the event. This can be anything, though we suggest making it JSON serializable.  |
        +-----------+------+-----------------------------------------------------------------------------------------------------------+

        Here are declarations associated with the standard events shown above:

        `format_docs`:

        .. code-block:: python

            def format_docs(docs: List[Document]) -> str:
                '''Format the docs.'''
                return ", ".join([doc.page_content for doc in docs])

            format_docs = RunnableLambda(format_docs)

        `some_tool`:

        .. code-block:: python

            @tool
            def some_tool(x: int, y: str) -> dict:
                '''Some_tool.'''
                return {"x": x, "y": y}

        `prompt`:

        .. code-block:: python

            template = ChatPromptTemplate.from_messages(
                [("system", "You are Cat Agent 007"), ("human", "{question}")]
            ).with_config({"run_name": "my_template", "tags": ["my_template"]})


        Example:

        .. code-block:: python

            from langchain_core.runnables import RunnableLambda

            async def reverse(s: str) -> str:
                return s[::-1]

            chain = RunnableLambda(func=reverse)

            events = [
                event async for event in chain.astream_events("hello", version="v2")
            ]

            # will produce the following events (run_id, and parent_ids
            # has been omitted for brevity):
            [
                {
                    "data": {"input": "hello"},
                    "event": "on_chain_start",
                    "metadata": {},
                    "name": "reverse",
                    "tags": [],
                },
                {
                    "data": {"chunk": "olleh"},
                    "event": "on_chain_stream",
                    "metadata": {},
                    "name": "reverse",
                    "tags": [],
                },
                {
                    "data": {"output": "olleh"},
                    "event": "on_chain_end",
                    "metadata": {},
                    "name": "reverse",
                    "tags": [],
                },
            ]


        Example: Dispatch Custom Event

        .. code-block:: python

            from langchain_core.callbacks.manager import (
                adispatch_custom_event,
            )
            from langchain_core.runnables import RunnableLambda, RunnableConfig
            import asyncio


            async def slow_thing(some_input: str, config: RunnableConfig) -> str:
                """Do something that takes a long time."""
                await asyncio.sleep(1) # Placeholder for some slow operation
                await adispatch_custom_event(
                    "progress_event",
                    {"message": "Finished step 1 of 3"},
                    config=config # Must be included for python < 3.10
                )
                await asyncio.sleep(1) # Placeholder for some slow operation
                await adispatch_custom_event(
                    "progress_event",
                    {"message": "Finished step 2 of 3"},
                    config=config # Must be included for python < 3.10
                )
                await asyncio.sleep(1) # Placeholder for some slow operation
                return "Done"

            slow_thing = RunnableLambda(slow_thing)

            async for event in slow_thing.astream_events("some_input", version="v2"):
                print(event)

        Args:
            input: The input to the Runnable.
            config: The config to use for the Runnable.
            version: The version of the schema to use either `v2` or `v1`.
                     Users should use `v2`.
                     `v1` is for backwards compatibility and will be deprecated
                     in 0.4.0.
                     No default will be assigned until the API is stabilized.
                     custom events will only be surfaced in `v2`.
            include_names: Only include events from runnables with matching names.
            include_types: Only include events from runnables with matching types.
            include_tags: Only include events from runnables with matching tags.
            exclude_names: Exclude events from runnables with matching names.
            exclude_types: Exclude events from runnables with matching types.
            exclude_tags: Exclude events from runnables with matching tags.
            kwargs: Additional keyword arguments to pass to the Runnable.
                These will be passed to astream_log as this implementation
                of astream_events is built on top of astream_log.

        Yields:
            An async stream of StreamEvents.

        Raises:
            NotImplementedError: If the version is not `v1` or `v2`.

###### Parameters

- **input**: The input to the Runnable.
- **config**: RunnableConfig) -> str:
                """Do something that takes a long time."""
                await asyncio.sleep(1) # Placeholder for some slow operation
                await adispatch_custom_event(
                    "progress_event",
                    {"message": "Finished step 1 of 3"},
                    config=config # Must be included for python < 3.10
                )
                await asyncio.sleep(1) # Placeholder for some slow operation
                await adispatch_custom_event(
                    "progress_event",
                    {"message": "Finished step 2 of 3"},
                    config=config # Must be included for python < 3.10
                )
                await asyncio.sleep(1) # Placeholder for some slow operation
                return "Done"

            slow_thing = RunnableLambda(slow_thing)

            async for event in slow_thing.astream_events("some_input", version="v2"):
                print(event)
- **version**: The version of the schema to use either `v2` or `v1`.
                     Users should use `v2`.
                     `v1` is for backwards compatibility and will be deprecated
                     in 0.4.0.
                     No default will be assigned until the API is stabilized.
                     custom events will only be surfaced in `v2`.
- **include_names**: Only include events from runnables with matching names.
- **include_types**: Only include events from runnables with matching types.
- **include_tags**: Only include events from runnables with matching tags.
- **exclude_names**: Exclude events from runnables with matching names.
- **exclude_types**: Exclude events from runnables with matching types.
- **exclude_tags**: Exclude events from runnables with matching tags.
- **kwargs**: Additional keyword arguments to pass to the Runnable.
                These will be passed to astream_log as this implementation
                of astream_events is built on top of astream_log.

##### astream_log

```python
astream_log(self, input: 'Any', config: 'Optional[RunnableConfig]' = None, diff: 'bool' = True, with_streamed_output_list: 'bool' = True, include_names: 'Optional[Sequence[str]]' = None, include_types: 'Optional[Sequence[str]]' = None, include_tags: 'Optional[Sequence[str]]' = None, exclude_names: 'Optional[Sequence[str]]' = None, exclude_types: 'Optional[Sequence[str]]' = None, exclude_tags: 'Optional[Sequence[str]]' = None, **kwargs: 'Any')
```

Stream all output from a Runnable, as reported to the callback system.
        This includes all inner runs of LLMs, Retrievers, Tools, etc.

        Output is streamed as Log objects, which include a list of
        Jsonpatch ops that describe how the state of the run has changed in each
        step, and the final state of the run.

        The Jsonpatch ops can be applied in order to construct state.

        Args:
            input: The input to the Runnable.
            config: The config to use for the Runnable.
            diff: Whether to yield diffs between each step or the current state.
            with_streamed_output_list: Whether to yield the streamed_output list.
            include_names: Only include logs with these names.
            include_types: Only include logs with these types.
            include_tags: Only include logs with these tags.
            exclude_names: Exclude logs with these names.
            exclude_types: Exclude logs with these types.
            exclude_tags: Exclude logs with these tags.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            A RunLogPatch or RunLog object.

###### Parameters

- **input**: The input to the Runnable.
- **config**: The config to use for the Runnable.
- **diff**: Whether to yield diffs between each step or the current state.
- **with_streamed_output_list**: Whether to yield the streamed_output list.
- **include_names**: Only include logs with these names.
- **include_types**: Only include logs with these types.
- **include_tags**: Only include logs with these tags.
- **exclude_names**: Exclude logs with these names.
- **exclude_types**: Exclude logs with these types.
- **exclude_tags**: Exclude logs with these tags.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### atransform

```python
atransform(self, input: 'AsyncIterator[Input]', config: 'Optional[RunnableConfig]' = None, **kwargs: 'Optional[Any]')
```

Default implementation of atransform, which buffers input and calls astream.
        Subclasses should override this method if they can start producing output while
        input is still being generated.

        Args:
            input: An async iterator of inputs to the Runnable.
            config: The config to use for the Runnable. Defaults to None.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            The output of the Runnable.

###### Parameters

- **input**: An async iterator of inputs to the Runnable.
- **config**: The config to use for the Runnable. Defaults to None.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### batch

```python
batch(self, inputs: 'list[LanguageModelInput]', config: 'Optional[Union[RunnableConfig, list[RunnableConfig]]]' = None, return_exceptions: 'bool' = False, **kwargs: 'Any')
```

##### batch_as_completed

```python
batch_as_completed(self, inputs: 'Sequence[Input]', config: 'Optional[Union[RunnableConfig, Sequence[RunnableConfig]]]' = None, return_exceptions: 'bool' = False, **kwargs: 'Optional[Any]')
```

Run invoke in parallel on a list of inputs,
        yielding results as they complete.

##### bind

```python
bind(self, **kwargs: 'Any')
```

Bind arguments to a Runnable, returning a new Runnable.

        Useful when a Runnable in a chain requires an argument that is not
        in the output of the previous Runnable or included in the user input.

        Args:
            kwargs: The arguments to bind to the Runnable.

        Returns:
            A new Runnable with the arguments bound.

        Example:

        .. code-block:: python

            from langchain_community.chat_models import ChatOllama
            from langchain_core.output_parsers import StrOutputParser

            llm = ChatOllama(model='llama2')

            # Without bind.
            chain = (
                llm
                | StrOutputParser()
            )

            chain.invoke("Repeat quoted words exactly: 'One two three four five.'")
            # Output is 'One two three four five.'

            # With bind.
            chain = (
                llm.bind(stop=["three"])
                | StrOutputParser()
            )

            chain.invoke("Repeat quoted words exactly: 'One two three four five.'")
            # Output is 'One two'

###### Parameters

- **kwargs**: The arguments to bind to the Runnable.

###### Returns

A new Runnable with the arguments bound.

##### config_schema

```python
config_schema(self, include: 'Optional[Sequence[str]]' = None)
```

The type of config this Runnable accepts specified as a pydantic model.

        To mark a field as configurable, see the `configurable_fields`
        and `configurable_alternatives` methods.

        Args:
            include: A list of fields to include in the config schema.

        Returns:
            A pydantic model that can be used to validate config.

###### Parameters

- **include**: A list of fields to include in the config schema.

###### Returns

A pydantic model that can be used to validate config.

##### configurable_alternatives

```python
configurable_alternatives(self, which: 'ConfigurableField', default_key: 'str' = 'default', prefix_keys: 'bool' = False, **kwargs: 'Union[Runnable[Input, Output], Callable[[], Runnable[Input, Output]]]')
```

Configure alternatives for Runnables that can be set at runtime.

        Args:
            which: The ConfigurableField instance that will be used to select the
                alternative.
            default_key: The default key to use if no alternative is selected.
                Defaults to "default".
            prefix_keys: Whether to prefix the keys with the ConfigurableField id.
                Defaults to False.
            **kwargs: A dictionary of keys to Runnable instances or callables that
                return Runnable instances.

        Returns:
            A new Runnable with the alternatives configured.

        .. code-block:: python

            from langchain_anthropic import ChatAnthropic
            from langchain_core.runnables.utils import ConfigurableField
            from langchain_openai import ChatOpenAI

            model = ChatAnthropic(
                model_name="claude-3-sonnet-20240229"
            ).configurable_alternatives(
                ConfigurableField(id="llm"),
                default_key="anthropic",
                openai=ChatOpenAI()
            )

            # uses the default model ChatAnthropic
            print(model.invoke("which organization created you?").content)

            # uses ChatOpenAI
            print(
                model.with_config(
                    configurable={"llm": "openai"}
                ).invoke("which organization created you?").content
            )

###### Parameters

- **which**: The ConfigurableField instance that will be used to select the
                alternative.
- **default_key**: The default key to use if no alternative is selected.
                Defaults to "default".
- **prefix_keys**: Whether to prefix the keys with the ConfigurableField id.
                Defaults to False.
            **kwargs: A dictionary of keys to Runnable instances or callables that
                return Runnable instances.

###### Returns

A new Runnable with the alternatives configured.

        .. code-block:: python

            from langchain_anthropic import ChatAnthropic
            from langchain_core.runnables.utils import ConfigurableField
            from langchain_openai import ChatOpenAI

            model = ChatAnthropic(
                model_name="claude-3-sonnet-20240229"
            ).configurable_alternatives(
                ConfigurableField(id="llm"),
                default_key="anthropic",
                openai=ChatOpenAI()
            )

            # uses the default model ChatAnthropic
            print(model.invoke("which organization created you?").content)

            # uses ChatOpenAI
            print(
                model.with_config(
                    configurable={"llm": "openai"}
                ).invoke("which organization created you?").content
            )

##### configurable_fields

```python
configurable_fields(self, **kwargs: 'AnyConfigurableField')
```

Configure particular Runnable fields at runtime.

        Args:
            **kwargs: A dictionary of ConfigurableField instances to configure.

        Returns:
            A new Runnable with the fields configured.

        .. code-block:: python

            from langchain_core.runnables import ConfigurableField
            from langchain_openai import ChatOpenAI

            model = ChatOpenAI(max_tokens=20).configurable_fields(
                max_tokens=ConfigurableField(
                    id="output_token_number",
                    name="Max tokens in the output",
                    description="The maximum number of tokens in the output",
                )
            )

            # max_tokens = 20
            print(
                "max_tokens_20: ",
                model.invoke("tell me something about chess").content
            )

            # max_tokens = 200
            print("max_tokens_200: ", model.with_config(
                configurable={"output_token_number": 200}
                ).invoke("tell me something about chess").content
            )

###### Parameters


###### Returns

A new Runnable with the fields configured.

        .. code-block:: python

            from langchain_core.runnables import ConfigurableField
            from langchain_openai import ChatOpenAI

            model = ChatOpenAI(max_tokens=20).configurable_fields(
                max_tokens=ConfigurableField(
                    id="output_token_number",
                    name="Max tokens in the output",
                    description="The maximum number of tokens in the output",
                )
            )

            # max_tokens = 20
            print(
                "max_tokens_20: ",
                model.invoke("tell me something about chess").content
            )

            # max_tokens = 200
            print("max_tokens_200: ", model.with_config(
                configurable={"output_token_number": 200}
                ).invoke("tell me something about chess").content
            )

##### copy

```python
copy(self, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False)
```

Returns a copy of the model.

        !!! warning "Deprecated"
            This method is now deprecated; use `model_copy` instead.

        If you need `include` or `exclude`, use:

        ```python {test="skip" lint="skip"}
        data = self.model_dump(include=include, exclude=exclude, round_trip=True)
        data = {**data, **(update or {})}
        copied = self.model_validate(data)
        ```

        Args:
            include: Optional set or mapping specifying which fields to include in the copied model.
            exclude: Optional set or mapping specifying which fields to exclude in the copied model.
            update: Optional dictionary of field-value pairs to override field values in the copied model.
            deep: If True, the values of fields that are Pydantic models will be deep-copied.

        Returns:
            A copy of the model with included, excluded and updated fields as specified.

###### Parameters

- **include**: Optional set or mapping specifying which fields to include in the copied model.
- **exclude**: Optional set or mapping specifying which fields to exclude in the copied model.
- **update**: Optional dictionary of field-value pairs to override field values in the copied model.
- **deep**: If True, the values of fields that are Pydantic models will be deep-copied.

###### Returns

A copy of the model with included, excluded and updated fields as specified.

##### dict

```python
dict(self, **kwargs: 'Any')
```

Return a dictionary of the LLM.

##### generate

```python
generate(self, prompts: 'list[str]', stop: 'Optional[list[str]]' = None, callbacks: 'Optional[Union[Callbacks, list[Callbacks]]]' = None, tags: 'Optional[Union[list[str], list[list[str]]]]' = None, metadata: 'Optional[Union[dict[str, Any], list[dict[str, Any]]]]' = None, run_name: 'Optional[Union[str, list[str]]]' = None, run_id: 'Optional[Union[uuid.UUID, list[Optional[uuid.UUID]]]]' = None, **kwargs: 'Any')
```

Pass a sequence of prompts to a model and return generations.

        This method should make use of batched calls for models that expose a batched
        API.

        Use this method when you want to:
            1. take advantage of batched calls,
            2. need more output from the model than just the top generated value,
            3. are building chains that are agnostic to the underlying language model
                type (e.g., pure text completion models vs chat models).

        Args:
            prompts: List of string prompts.
            stop: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of these substrings.
            callbacks: Callbacks to pass through. Used for executing additional
                functionality, such as logging or streaming, throughout generation.
            tags: List of tags to associate with each prompt. If provided, the length
                of the list must match the length of the prompts list.
            metadata: List of metadata dictionaries to associate with each prompt. If
                provided, the length of the list must match the length of the prompts
                list.
            run_name: List of run names to associate with each prompt. If provided, the
                length of the list must match the length of the prompts list.
            run_id: List of run IDs to associate with each prompt. If provided, the
                length of the list must match the length of the prompts list.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            An LLMResult, which contains a list of candidate Generations for each input
                prompt and additional model provider-specific output.

###### Parameters

- **prompts**: List of string prompts.
- **stop**: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of these substrings.
- **callbacks**: Callbacks to pass through. Used for executing additional
                functionality, such as logging or streaming, throughout generation.
- **tags**: List of tags to associate with each prompt. If provided, the length
                of the list must match the length of the prompts list.
- **metadata**: List of metadata dictionaries to associate with each prompt. If
                provided, the length of the list must match the length of the prompts
                list.
- **run_name**: List of run names to associate with each prompt. If provided, the
                length of the list must match the length of the prompts list.
- **run_id**: List of run IDs to associate with each prompt. If provided, the
                length of the list must match the length of the prompts list.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

###### Returns

An LLMResult, which contains a list of candidate Generations for each input
                prompt and additional model provider-specific output.

##### generate_prompt

```python
generate_prompt(self, prompts: 'list[PromptValue]', stop: 'Optional[list[str]]' = None, callbacks: 'Optional[Union[Callbacks, list[Callbacks]]]' = None, **kwargs: 'Any')
```

##### get_config_jsonschema

```python
get_config_jsonschema(self, include: 'Optional[Sequence[str]]' = None)
```

Get a JSON schema that represents the config of the Runnable.

        Args:
            include: A list of fields to include in the config schema.

        Returns:
            A JSON schema that represents the config of the Runnable.

        .. versionadded:: 0.3.0

###### Parameters

- **include**: A list of fields to include in the config schema.

###### Returns

A JSON schema that represents the config of the Runnable.

        .. versionadded:: 0.3.0

##### get_graph

```python
get_graph(self, config: 'Optional[RunnableConfig]' = None)
```

Return a graph representation of this Runnable.

##### get_input_jsonschema

```python
get_input_jsonschema(self, config: 'Optional[RunnableConfig]' = None)
```

Get a JSON schema that represents the input to the Runnable.

        Args:
            config: A config to use when generating the schema.

        Returns:
            A JSON schema that represents the input to the Runnable.

        Example:

            .. code-block:: python

                from langchain_core.runnables import RunnableLambda

                def add_one(x: int) -> int:
                    return x + 1

                runnable = RunnableLambda(add_one)

                print(runnable.get_input_jsonschema())

        .. versionadded:: 0.3.0

###### Parameters

- **config**: A config to use when generating the schema.

###### Returns

A JSON schema that represents the input to the Runnable.

##### get_input_schema

```python
get_input_schema(self, config: 'Optional[RunnableConfig]' = None)
```

Get a pydantic model that can be used to validate input to the Runnable.

        Runnables that leverage the configurable_fields and configurable_alternatives
        methods will have a dynamic input schema that depends on which
        configuration the Runnable is invoked with.

        This method allows to get an input schema for a specific configuration.

        Args:
            config: A config to use when generating the schema.

        Returns:
            A pydantic model that can be used to validate input.

###### Parameters

- **config**: A config to use when generating the schema.

###### Returns

A pydantic model that can be used to validate input.

##### get_name

```python
get_name(self, suffix: 'Optional[str]' = None, name: 'Optional[str]' = None)
```

Get the name of the Runnable.

##### get_num_tokens

```python
get_num_tokens(self, text: 'str')
```

Get the number of tokens present in the text.

        Useful for checking if an input fits in a model's context window.

        Args:
            text: The string input to tokenize.

        Returns:
            The integer number of tokens in the text.

###### Parameters

- **text**: The string input to tokenize.

###### Returns

The integer number of tokens in the text.

##### get_num_tokens_from_messages

```python
get_num_tokens_from_messages(self, messages: 'list[BaseMessage]', tools: 'Optional[Sequence]' = None)
```

Get the number of tokens in the messages.

        Useful for checking if an input fits in a model's context window.

        **Note**: the base implementation of get_num_tokens_from_messages ignores
        tool schemas.

        Args:
            messages: The message inputs to tokenize.
            tools: If provided, sequence of dict, BaseModel, function, or BaseTools
                to be converted to tool schemas.

        Returns:
            The sum of the number of tokens across the messages.

###### Parameters

- **messages**: The message inputs to tokenize.
- **tools**: If provided, sequence of dict, BaseModel, function, or BaseTools
                to be converted to tool schemas.

###### Returns

The sum of the number of tokens across the messages.

##### get_output_jsonschema

```python
get_output_jsonschema(self, config: 'Optional[RunnableConfig]' = None)
```

Get a JSON schema that represents the output of the Runnable.

        Args:
            config: A config to use when generating the schema.

        Returns:
            A JSON schema that represents the output of the Runnable.

        Example:

            .. code-block:: python

                from langchain_core.runnables import RunnableLambda

                def add_one(x: int) -> int:
                    return x + 1

                runnable = RunnableLambda(add_one)

                print(runnable.get_output_jsonschema())

        .. versionadded:: 0.3.0

###### Parameters

- **config**: A config to use when generating the schema.

###### Returns

A JSON schema that represents the output of the Runnable.

##### get_output_schema

```python
get_output_schema(self, config: 'Optional[RunnableConfig]' = None)
```

Get a pydantic model that can be used to validate output to the Runnable.

        Runnables that leverage the configurable_fields and configurable_alternatives
        methods will have a dynamic output schema that depends on which
        configuration the Runnable is invoked with.

        This method allows to get an output schema for a specific configuration.

        Args:
            config: A config to use when generating the schema.

        Returns:
            A pydantic model that can be used to validate output.

###### Parameters

- **config**: A config to use when generating the schema.

###### Returns

A pydantic model that can be used to validate output.

##### get_prompts

```python
get_prompts(self, config: 'Optional[RunnableConfig]' = None)
```

Return a list of prompts used by this Runnable.

##### get_token_ids

```python
get_token_ids(self, text: 'str')
```

Return the ordered ids of the tokens in a text.

        Args:
            text: The string input to tokenize.

        Returns:
            A list of ids corresponding to the tokens in the text, in order they occur
                in the text.

###### Parameters

- **text**: The string input to tokenize.

###### Returns

A list of ids corresponding to the tokens in the text, in order they occur
                in the text.

##### invoke

```python
invoke(self, input: 'LanguageModelInput', config: 'Optional[RunnableConfig]' = None, stop: 'Optional[list[str]]' = None, **kwargs: 'Any')
```

##### json

```python
json(self, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any')
```

##### map

```python
map(self)
```

Return a new Runnable that maps a list of inputs to a list of outputs,
        by calling invoke() with each input.

        Returns:
            A new Runnable that maps a list of inputs to a list of outputs.

        Example:

            .. code-block:: python

                    from langchain_core.runnables import RunnableLambda

                    def _lambda(x: int) -> int:
                        return x + 1

                    runnable = RunnableLambda(_lambda)
                    print(runnable.map().invoke([1, 2, 3])) # [2, 3, 4]

###### Returns

A new Runnable that maps a list of inputs to a list of outputs.

##### model_copy

```python
model_copy(self, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False)
```

Usage docs: https://docs.pydantic.dev/2.10/concepts/serialization/#model_copy

        Returns a copy of the model.

        Args:
            update: Values to change/add in the new model. Note: the data is not validated
                before creating the new model. You should trust this data.
            deep: Set to `True` to make a deep copy of the model.

        Returns:
            New model instance.

###### Parameters

- **update**: Values to change/add in the new model. Note: the data is not validated
                before creating the new model. You should trust this data.
- **deep**: Set to `True` to make a deep copy of the model.

###### Returns

New model instance.

##### model_dump

```python
model_dump(self, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, serialize_as_any: 'bool' = False)
```

Usage docs: https://docs.pydantic.dev/2.10/concepts/serialization/#modelmodel_dump

        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        Args:
            mode: The mode in which `to_python` should run.
                If mode is 'json', the output will only contain JSON serializable types.
                If mode is 'python', the output may contain non-JSON-serializable Python objects.
            include: A set of fields to include in the output.
            exclude: A set of fields to exclude from the output.
            context: Additional context to pass to the serializer.
            by_alias: Whether to use the field's alias in the dictionary key if defined.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of `None`.
            round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
            warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
            serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

        Returns:
            A dictionary representation of the model.

###### Parameters

- **mode**: The mode in which `to_python` should run.
                If mode is 'json', the output will only contain JSON serializable types.
                If mode is 'python', the output may contain non-JSON-serializable Python objects.
- **include**: A set of fields to include in the output.
- **exclude**: A set of fields to exclude from the output.
- **context**: Additional context to pass to the serializer.
- **by_alias**: Whether to use the field's alias in the dictionary key if defined.
- **exclude_unset**: Whether to exclude fields that have not been explicitly set.
- **exclude_defaults**: Whether to exclude fields that are set to their default value.
- **exclude_none**: Whether to exclude fields that have a value of `None`.
- **round_trip**: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- **warnings**: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- **serialize_as_any**: Whether to serialize fields with duck-typing serialization behavior.

###### Returns

A dictionary representation of the model.

##### model_dump_json

```python
model_dump_json(self, indent: 'int | None' = None, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, serialize_as_any: 'bool' = False)
```

Usage docs: https://docs.pydantic.dev/2.10/concepts/serialization/#modelmodel_dump_json

        Generates a JSON representation of the model using Pydantic's `to_json` method.

        Args:
            indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
            include: Field(s) to include in the JSON output.
            exclude: Field(s) to exclude from the JSON output.
            context: Additional context to pass to the serializer.
            by_alias: Whether to serialize using field aliases.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of `None`.
            round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
            warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
            serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

        Returns:
            A JSON string representation of the model.

###### Parameters

- **indent**: Indentation to use in the JSON output. If None is passed, the output will be compact.
- **include**: Field(s) to include in the JSON output.
- **exclude**: Field(s) to exclude from the JSON output.
- **context**: Additional context to pass to the serializer.
- **by_alias**: Whether to serialize using field aliases.
- **exclude_unset**: Whether to exclude fields that have not been explicitly set.
- **exclude_defaults**: Whether to exclude fields that are set to their default value.
- **exclude_none**: Whether to exclude fields that have a value of `None`.
- **round_trip**: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- **warnings**: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- **serialize_as_any**: Whether to serialize fields with duck-typing serialization behavior.

###### Returns

A JSON string representation of the model.

##### model_post_init

```python
model_post_init(self: 'BaseModel', context: 'Any')
```

This function is meant to behave like a BaseModel method to initialise private attributes.

    It takes context as an argument since that's what pydantic-core passes when calling it.

    Args:
        self: The BaseModel instance.
        context: The context.

###### Parameters

- **context**: The context.

##### pick

```python
pick(self, keys: 'Union[str, list[str]]')
```

Pick keys from the output dict of this Runnable.

        Pick single key:
            .. code-block:: python

                import json

                from langchain_core.runnables import RunnableLambda, RunnableMap

                as_str = RunnableLambda(str)
                as_json = RunnableLambda(json.loads)
                chain = RunnableMap(str=as_str, json=as_json)

                chain.invoke("[1, 2, 3]")
                # -> {"str": "[1, 2, 3]", "json": [1, 2, 3]}

                json_only_chain = chain.pick("json")
                json_only_chain.invoke("[1, 2, 3]")
                # -> [1, 2, 3]

        Pick list of keys:
            .. code-block:: python

                from typing import Any

                import json

                from langchain_core.runnables import RunnableLambda, RunnableMap

                as_str = RunnableLambda(str)
                as_json = RunnableLambda(json.loads)
                def as_bytes(x: Any) -> bytes:
                    return bytes(x, "utf-8")

                chain = RunnableMap(
                    str=as_str,
                    json=as_json,
                    bytes=RunnableLambda(as_bytes)
                )

                chain.invoke("[1, 2, 3]")
                # -> {"str": "[1, 2, 3]", "json": [1, 2, 3], "bytes": b"[1, 2, 3]"}

                json_and_bytes_chain = chain.pick(["json", "bytes"])
                json_and_bytes_chain.invoke("[1, 2, 3]")
                # -> {"json": [1, 2, 3], "bytes": b"[1, 2, 3]"}

##### pipe

```python
pipe(self, *others: 'Union[Runnable[Any, Other], Callable[[Any], Other]]', name: 'Optional[str]' = None)
```

Compose this Runnable with Runnable-like objects to make a RunnableSequence.

        Equivalent to `RunnableSequence(self, *others)` or `self | others[0] | ...`

        Example:
            .. code-block:: python

                from langchain_core.runnables import RunnableLambda

                def add_one(x: int) -> int:
                    return x + 1

                def mul_two(x: int) -> int:
                    return x * 2

                runnable_1 = RunnableLambda(add_one)
                runnable_2 = RunnableLambda(mul_two)
                sequence = runnable_1.pipe(runnable_2)
                # Or equivalently:
                # sequence = runnable_1 | runnable_2
                # sequence = RunnableSequence(first=runnable_1, last=runnable_2)
                sequence.invoke(1)
                await sequence.ainvoke(1)
                # -> 4

                sequence.batch([1, 2, 3])
                await sequence.abatch([1, 2, 3])
                # -> [4, 6, 8]

##### predict

```python
predict(self, text: 'str', stop: 'Optional[Sequence[str]]' = None, **kwargs: 'Any')
```

.. deprecated:: 0.1.7 Use :meth:`~invoke` instead. It will not be removed until langchain-core==1.0.

##### predict_messages

```python
predict_messages(self, messages: 'list[BaseMessage]', stop: 'Optional[Sequence[str]]' = None, **kwargs: 'Any')
```

.. deprecated:: 0.1.7 Use :meth:`~invoke` instead. It will not be removed until langchain-core==1.0.

##### save

```python
save(self, file_path: 'Union[Path, str]')
```

Save the LLM.

        Args:
            file_path: Path to file to save the LLM to.

        Raises:
            ValueError: If the file path is not a string or Path object.

        Example:
        .. code-block:: python

            llm.save(file_path="path/llm.yaml")

###### Parameters

- **file_path**: Path to file to save the LLM to.

##### stream

```python
stream(self, input: 'LanguageModelInput', config: 'Optional[RunnableConfig]' = None, stop: 'Optional[list[str]]' = None, **kwargs: 'Any')
```

##### to_json

```python
to_json(self)
```

Serialize the Runnable to JSON.

        Returns:
            A JSON-serializable representation of the Runnable.

###### Returns

A JSON-serializable representation of the Runnable.

##### to_json_not_implemented

```python
to_json_not_implemented(self)
```

##### transform

```python
transform(self, input: 'Iterator[Input]', config: 'Optional[RunnableConfig]' = None, **kwargs: 'Optional[Any]')
```

Default implementation of transform, which buffers input and calls astream.

        Subclasses should override this method if they can start producing output while
        input is still being generated.

        Args:
            input: An iterator of inputs to the Runnable.
            config: The config to use for the Runnable. Defaults to None.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            The output of the Runnable.

###### Parameters

- **input**: An iterator of inputs to the Runnable.
- **config**: The config to use for the Runnable. Defaults to None.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### with_alisteners

```python
with_alisteners(self, on_start: 'Optional[AsyncListener]' = None, on_end: 'Optional[AsyncListener]' = None, on_error: 'Optional[AsyncListener]' = None)
```

Bind async lifecycle listeners to a Runnable, returning a new Runnable.

        on_start: Asynchronously called before the Runnable starts running.
        on_end: Asynchronously called after the Runnable finishes running.
        on_error: Asynchronously called if the Runnable throws an error.

        The Run object contains information about the run, including its id,
        type, input, output, error, start_time, end_time, and any tags or metadata
        added to the run.

        Args:
            on_start: Asynchronously called before the Runnable starts running.
                Defaults to None.
            on_end: Asynchronously called after the Runnable finishes running.
                Defaults to None.
            on_error: Asynchronously called if the Runnable throws an error.
                Defaults to None.

        Returns:
            A new Runnable with the listeners bound.

        Example:

        .. code-block:: python

            from langchain_core.runnables import RunnableLambda
            import time

            async def test_runnable(time_to_sleep : int):
                print(f"Runnable[{time_to_sleep}s]: starts at {format_t(time.time())}")
                await asyncio.sleep(time_to_sleep)
                print(f"Runnable[{time_to_sleep}s]: ends at {format_t(time.time())}")

            async def fn_start(run_obj : Runnable):
                print(f"on start callback starts at {format_t(time.time())}
                await asyncio.sleep(3)
                print(f"on start callback ends at {format_t(time.time())}")

            async def fn_end(run_obj : Runnable):
                print(f"on end callback starts at {format_t(time.time())}
                await asyncio.sleep(2)
                print(f"on end callback ends at {format_t(time.time())}")

            runnable = RunnableLambda(test_runnable).with_alisteners(
                on_start=fn_start,
                on_end=fn_end
            )
            async def concurrent_runs():
                await asyncio.gather(runnable.ainvoke(2), runnable.ainvoke(3))

            asyncio.run(concurrent_runs())
            Result:
            on start callback starts at 2024-05-16T14:20:29.637053+00:00
            on start callback starts at 2024-05-16T14:20:29.637150+00:00
            on start callback ends at 2024-05-16T14:20:32.638305+00:00
            on start callback ends at 2024-05-16T14:20:32.638383+00:00
            Runnable[3s]: starts at 2024-05-16T14:20:32.638849+00:00
            Runnable[5s]: starts at 2024-05-16T14:20:32.638999+00:00
            Runnable[3s]: ends at 2024-05-16T14:20:35.640016+00:00
            on end callback starts at 2024-05-16T14:20:35.640534+00:00
            Runnable[5s]: ends at 2024-05-16T14:20:37.640169+00:00
            on end callback starts at 2024-05-16T14:20:37.640574+00:00
            on end callback ends at 2024-05-16T14:20:37.640654+00:00
            on end callback ends at 2024-05-16T14:20:39.641751+00:00

###### Parameters

- **on_start**: Asynchronously called before the Runnable starts running.
- **on_end**: Asynchronously called after the Runnable finishes running.
- **on_error**: Asynchronously called if the Runnable throws an error.

        The Run object contains information about the run, including its id,
        type, input, output, error, start_time, end_time, and any tags or metadata
        added to the run.

###### Returns

A new Runnable with the listeners bound.

##### with_config

```python
with_config(self, config: 'Optional[RunnableConfig]' = None, **kwargs: 'Any')
```

Bind config to a Runnable, returning a new Runnable.

        Args:
            config: The config to bind to the Runnable.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Returns:
            A new Runnable with the config bound.

###### Parameters

- **config**: The config to bind to the Runnable.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

###### Returns

A new Runnable with the config bound.

##### with_fallbacks

```python
with_fallbacks(self, fallbacks: 'Sequence[Runnable[Input, Output]]', exceptions_to_handle: 'tuple[type[BaseException], ...]' = (<class 'Exception'>,), exception_key: 'Optional[str]' = None)
```

Add fallbacks to a Runnable, returning a new Runnable.

        The new Runnable will try the original Runnable, and then each fallback
        in order, upon failures.

        Args:
            fallbacks: A sequence of runnables to try if the original Runnable fails.
            exceptions_to_handle: A tuple of exception types to handle.
                Defaults to (Exception,).
            exception_key: If string is specified then handled exceptions will be passed
                to fallbacks as part of the input under the specified key. If None,
                exceptions will not be passed to fallbacks. If used, the base Runnable
                and its fallbacks must accept a dictionary as input. Defaults to None.

        Returns:
            A new Runnable that will try the original Runnable, and then each
            fallback in order, upon failures.

        Example:

            .. code-block:: python

                from typing import Iterator

                from langchain_core.runnables import RunnableGenerator


                def _generate_immediate_error(input: Iterator) -> Iterator[str]:
                    raise ValueError()
                    yield ""


                def _generate(input: Iterator) -> Iterator[str]:
                    yield from "foo bar"


                runnable = RunnableGenerator(_generate_immediate_error).with_fallbacks(
                    [RunnableGenerator(_generate)]
                    )
                print(''.join(runnable.stream({}))) #foo bar

        Args:
            fallbacks: A sequence of runnables to try if the original Runnable fails.
            exceptions_to_handle: A tuple of exception types to handle.
            exception_key: If string is specified then handled exceptions will be passed
                to fallbacks as part of the input under the specified key. If None,
                exceptions will not be passed to fallbacks. If used, the base Runnable
                and its fallbacks must accept a dictionary as input.

        Returns:
            A new Runnable that will try the original Runnable, and then each
            fallback in order, upon failures.

###### Parameters

- **fallbacks**: A sequence of runnables to try if the original Runnable fails.
- **exceptions_to_handle**: A tuple of exception types to handle.
                Defaults to (Exception,).
- **exception_key**: If string is specified then handled exceptions will be passed
                to fallbacks as part of the input under the specified key. If None,
                exceptions will not be passed to fallbacks. If used, the base Runnable
                and its fallbacks must accept a dictionary as input. Defaults to None.

###### Returns

A new Runnable that will try the original Runnable, and then each
            fallback in order, upon failures.

##### with_listeners

```python
with_listeners(self, on_start: 'Optional[Union[Callable[[Run], None], Callable[[Run, RunnableConfig], None]]]' = None, on_end: 'Optional[Union[Callable[[Run], None], Callable[[Run, RunnableConfig], None]]]' = None, on_error: 'Optional[Union[Callable[[Run], None], Callable[[Run, RunnableConfig], None]]]' = None)
```

Bind lifecycle listeners to a Runnable, returning a new Runnable.

        on_start: Called before the Runnable starts running, with the Run object.
        on_end: Called after the Runnable finishes running, with the Run object.
        on_error: Called if the Runnable throws an error, with the Run object.

        The Run object contains information about the run, including its id,
        type, input, output, error, start_time, end_time, and any tags or metadata
        added to the run.

        Args:
            on_start: Called before the Runnable starts running. Defaults to None.
            on_end: Called after the Runnable finishes running. Defaults to None.
            on_error: Called if the Runnable throws an error. Defaults to None.

        Returns:
            A new Runnable with the listeners bound.

        Example:

        .. code-block:: python

            from langchain_core.runnables import RunnableLambda
            from langchain_core.tracers.schemas import Run

            import time

            def test_runnable(time_to_sleep : int):
                time.sleep(time_to_sleep)

            def fn_start(run_obj: Run):
                print("start_time:", run_obj.start_time)

            def fn_end(run_obj: Run):
                print("end_time:", run_obj.end_time)

            chain = RunnableLambda(test_runnable).with_listeners(
                on_start=fn_start,
                on_end=fn_end
            )
            chain.invoke(2)

###### Parameters

- **on_start**: Called before the Runnable starts running, with the Run object.
- **on_end**: Called after the Runnable finishes running, with the Run object.
- **on_error**: Called if the Runnable throws an error, with the Run object.

        The Run object contains information about the run, including its id,
        type, input, output, error, start_time, end_time, and any tags or metadata
        added to the run.

###### Returns

A new Runnable with the listeners bound.

##### with_retry

```python
with_retry(self, retry_if_exception_type: 'tuple[type[BaseException], ...]' = (<class 'Exception'>,), wait_exponential_jitter: 'bool' = True, stop_after_attempt: 'int' = 3)
```

Create a new Runnable that retries the original Runnable on exceptions.

        Args:
            retry_if_exception_type: A tuple of exception types to retry on.
                Defaults to (Exception,).
            wait_exponential_jitter: Whether to add jitter to the wait
                time between retries. Defaults to True.
            stop_after_attempt: The maximum number of attempts to make before
                giving up. Defaults to 3.

        Returns:
            A new Runnable that retries the original Runnable on exceptions.

        Example:

        .. code-block:: python

            from langchain_core.runnables import RunnableLambda

            count = 0


            def _lambda(x: int) -> None:
                global count
                count = count + 1
                if x == 1:
                    raise ValueError("x is 1")
                else:
                     pass


            runnable = RunnableLambda(_lambda)
            try:
                runnable.with_retry(
                    stop_after_attempt=2,
                    retry_if_exception_type=(ValueError,),
                ).invoke(1)
            except ValueError:
                pass

            assert (count == 2)


        Args:
            retry_if_exception_type: A tuple of exception types to retry on
            wait_exponential_jitter: Whether to add jitter to the wait time
                                     between retries
            stop_after_attempt: The maximum number of attempts to make before giving up

        Returns:
            A new Runnable that retries the original Runnable on exceptions.

###### Parameters

- **retry_if_exception_type**: A tuple of exception types to retry on.
                Defaults to (Exception,).
- **wait_exponential_jitter**: Whether to add jitter to the wait
                time between retries. Defaults to True.
- **stop_after_attempt**: The maximum number of attempts to make before
                giving up. Defaults to 3.

###### Returns

A new Runnable that retries the original Runnable on exceptions.

##### with_structured_output

```python
with_structured_output(self, schema: 'Union[dict, type]', **kwargs: 'Any')
```

Not implemented on this class.

##### with_types

```python
with_types(self, input_type: 'Optional[type[Input]]' = None, output_type: 'Optional[type[Output]]' = None)
```

Bind input and output types to a Runnable, returning a new Runnable.

        Args:
            input_type: The input type to bind to the Runnable. Defaults to None.
            output_type: The output type to bind to the Runnable. Defaults to None.

        Returns:
            A new Runnable with the types bound.

###### Parameters

- **input_type**: The input type to bind to the Runnable. Defaults to None.
- **output_type**: The output type to bind to the Runnable. Defaults to None.

###### Returns

A new Runnable with the types bound.

### PromptTemplate

Prompt template for a language model.

    A prompt template consists of a string template. It accepts a set of parameters
    from the user that can be used to generate a prompt for a language model.

    The template can be formatted using either f-strings (default), jinja2,
    or mustache syntax.

    *Security warning*:
        Prefer using `template_format="f-string"` instead of
        `template_format="jinja2"`, or make sure to NEVER accept jinja2 templates
        from untrusted sources as they may lead to arbitrary Python code execution.

        As of LangChain 0.0.329, Jinja2 templates will be rendered using
        Jinja2's SandboxedEnvironment by default. This sand-boxing should
        be treated as a best-effort approach rather than a guarantee of security,
        as it is an opt-out rather than opt-in approach.

        Despite the sand-boxing, we recommend to never use jinja2 templates
        from untrusted sources.

    Example:

        .. code-block:: python

            from langchain_core.prompts import PromptTemplate

            # Instantiation using from_template (recommended)
            prompt = PromptTemplate.from_template("Say {foo}")
            prompt.format(foo="bar")

            # Instantiation using initializer
            prompt = PromptTemplate(template="Say {foo}")

#### Methods

##### __init__

```python
__init__(self, *args: Any, **kwargs: Any)
```

##### abatch

```python
abatch(self, inputs: 'list[Input]', config: 'Optional[Union[RunnableConfig, list[RunnableConfig]]]' = None, return_exceptions: 'bool' = False, **kwargs: 'Optional[Any]')
```

Default implementation runs ainvoke in parallel using asyncio.gather.

        The default implementation of batch works well for IO bound runnables.

        Subclasses should override this method if they can batch more efficiently;
        e.g., if the underlying Runnable uses an API which supports a batch mode.

        Args:
            inputs: A list of inputs to the Runnable.
            config: A config to use when invoking the Runnable.
               The config supports standard keys like 'tags', 'metadata' for tracing
               purposes, 'max_concurrency' for controlling how much work to do
               in parallel, and other keys. Please refer to the RunnableConfig
               for more details. Defaults to None.
            return_exceptions: Whether to return exceptions instead of raising them.
                Defaults to False.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Returns:
            A list of outputs from the Runnable.

###### Parameters

- **inputs**: A list of inputs to the Runnable.
- **config**: A config to use when invoking the Runnable.
               The config supports standard keys like 'tags', 'metadata' for tracing
               purposes, 'max_concurrency' for controlling how much work to do
               in parallel, and other keys. Please refer to the RunnableConfig
               for more details. Defaults to None.
- **return_exceptions**: Whether to return exceptions instead of raising them.
                Defaults to False.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

###### Returns

A list of outputs from the Runnable.

##### abatch_as_completed

```python
abatch_as_completed(self, inputs: 'Sequence[Input]', config: 'Optional[Union[RunnableConfig, Sequence[RunnableConfig]]]' = None, return_exceptions: 'bool' = False, **kwargs: 'Optional[Any]')
```

Run ainvoke in parallel on a list of inputs,
        yielding results as they complete.

        Args:
            inputs: A list of inputs to the Runnable.
            config: A config to use when invoking the Runnable.
               The config supports standard keys like 'tags', 'metadata' for tracing
               purposes, 'max_concurrency' for controlling how much work to do
               in parallel, and other keys. Please refer to the RunnableConfig
               for more details. Defaults to None. Defaults to None.
            return_exceptions: Whether to return exceptions instead of raising them.
                Defaults to False.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            A tuple of the index of the input and the output from the Runnable.

###### Parameters

- **inputs**: A list of inputs to the Runnable.
- **config**: A config to use when invoking the Runnable.
               The config supports standard keys like 'tags', 'metadata' for tracing
               purposes, 'max_concurrency' for controlling how much work to do
               in parallel, and other keys. Please refer to the RunnableConfig
               for more details. Defaults to None. Defaults to None.
- **return_exceptions**: Whether to return exceptions instead of raising them.
                Defaults to False.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### aformat

```python
aformat(self, **kwargs: 'Any')
```

Async format the prompt with the inputs.

        Args:
            kwargs: Any arguments to be passed to the prompt template.

        Returns:
            A formatted string.

        Example:

        .. code-block:: python

            await prompt.aformat(variable1="foo")

###### Parameters

- **kwargs**: Any arguments to be passed to the prompt template.

###### Returns

A formatted string.

##### aformat_prompt

```python
aformat_prompt(self, **kwargs: 'Any')
```

Async format the prompt with the inputs.

        Args:
            kwargs: Any arguments to be passed to the prompt template.

        Returns:
            A formatted string.

###### Parameters

- **kwargs**: Any arguments to be passed to the prompt template.

###### Returns

A formatted string.

##### ainvoke

```python
ainvoke(self, input: 'dict', config: 'Optional[RunnableConfig]' = None, **kwargs: 'Any')
```

Async invoke the prompt.

        Args:
            input: Dict, input to the prompt.
            config: RunnableConfig, configuration for the prompt.

        Returns:
            PromptValue: The output of the prompt.

###### Parameters

- **input**: Dict, input to the prompt.
- **config**: RunnableConfig, configuration for the prompt.

###### Returns



##### as_tool

```python
as_tool(self, args_schema: 'Optional[type[BaseModel]]' = None, name: 'Optional[str]' = None, description: 'Optional[str]' = None, arg_types: 'Optional[dict[str, type]]' = None)
```

.. beta::
   This API is in beta and may change in the future.

Create a BaseTool from a Runnable.

``as_tool`` will instantiate a BaseTool with a name, description, and
``args_schema`` from a Runnable. Where possible, schemas are inferred
from ``runnable.get_input_schema``. Alternatively (e.g., if the
Runnable takes a dict as input and the specific dict keys are not typed),
the schema can be specified directly with ``args_schema``. You can also
pass ``arg_types`` to just specify the required arguments and their types.

Args:
    args_schema: The schema for the tool. Defaults to None.
    name: The name of the tool. Defaults to None.
    description: The description of the tool. Defaults to None.
    arg_types: A dictionary of argument names to types. Defaults to None.

Returns:
    A BaseTool instance.

Typed dict input:

.. code-block:: python

    from typing import List
    from typing_extensions import TypedDict
    from langchain_core.runnables import RunnableLambda

    class Args(TypedDict):
        a: int
        b: List[int]

    def f(x: Args) -> str:
        return str(x["a"] * max(x["b"]))

    runnable = RunnableLambda(f)
    as_tool = runnable.as_tool()
    as_tool.invoke({"a": 3, "b": [1, 2]})

``dict`` input, specifying schema via ``args_schema``:

.. code-block:: python

    from typing import Any, Dict, List
    from pydantic import BaseModel, Field
    from langchain_core.runnables import RunnableLambda

    def f(x: Dict[str, Any]) -> str:
        return str(x["a"] * max(x["b"]))

    class FSchema(BaseModel):
        """Apply a function to an integer and list of integers."""

        a: int = Field(..., description="Integer")
        b: List[int] = Field(..., description="List of ints")

    runnable = RunnableLambda(f)
    as_tool = runnable.as_tool(FSchema)
    as_tool.invoke({"a": 3, "b": [1, 2]})

``dict`` input, specifying schema via ``arg_types``:

.. code-block:: python

    from typing import Any, Dict, List
    from langchain_core.runnables import RunnableLambda

    def f(x: Dict[str, Any]) -> str:
        return str(x["a"] * max(x["b"]))

    runnable = RunnableLambda(f)
    as_tool = runnable.as_tool(arg_types={"a": int, "b": List[int]})
    as_tool.invoke({"a": 3, "b": [1, 2]})

String input:

.. code-block:: python

    from langchain_core.runnables import RunnableLambda

    def f(x: str) -> str:
        return x + "a"

    def g(x: str) -> str:
        return x + "z"

    runnable = RunnableLambda(f) | g
    as_tool = runnable.as_tool()
    as_tool.invoke("b")

.. versionadded:: 0.2.14

###### Parameters

- **args_schema**: The schema for the tool. Defaults to None.
- **name**: The name of the tool. Defaults to None.
- **description**: The description of the tool. Defaults to None.
- **arg_types**: A dictionary of argument names to types. Defaults to None.

###### Returns

A BaseTool instance.

Typed dict input:

.. code-block:: python

    from typing import List
    from typing_extensions import TypedDict
    from langchain_core.runnables import RunnableLambda

    class Args(TypedDict):

##### assign

```python
assign(self, **kwargs: 'Union[Runnable[dict[str, Any], Any], Callable[[dict[str, Any]], Any], Mapping[str, Union[Runnable[dict[str, Any], Any], Callable[[dict[str, Any]], Any]]]]')
```

Assigns new fields to the dict output of this Runnable.
        Returns a new Runnable.

        .. code-block:: python

            from langchain_community.llms.fake import FakeStreamingListLLM
            from langchain_core.output_parsers import StrOutputParser
            from langchain_core.prompts import SystemMessagePromptTemplate
            from langchain_core.runnables import Runnable
            from operator import itemgetter

            prompt = (
                SystemMessagePromptTemplate.from_template("You are a nice assistant.")
                + "{question}"
            )
            llm = FakeStreamingListLLM(responses=["foo-lish"])

            chain: Runnable = prompt | llm | {"str": StrOutputParser()}

            chain_with_assign = chain.assign(hello=itemgetter("str") | llm)

            print(chain_with_assign.input_schema.model_json_schema())
            # {'title': 'PromptInput', 'type': 'object', 'properties':
            {'question': {'title': 'Question', 'type': 'string'}}}
            print(chain_with_assign.output_schema.model_json_schema())
            # {'title': 'RunnableSequenceOutput', 'type': 'object', 'properties':
            {'str': {'title': 'Str',
            'type': 'string'}, 'hello': {'title': 'Hello', 'type': 'string'}}}

##### astream

```python
astream(self, input: 'Input', config: 'Optional[RunnableConfig]' = None, **kwargs: 'Optional[Any]')
```

Default implementation of astream, which calls ainvoke.
        Subclasses should override this method if they support streaming output.

        Args:
            input: The input to the Runnable.
            config: The config to use for the Runnable. Defaults to None.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            The output of the Runnable.

###### Parameters

- **input**: The input to the Runnable.
- **config**: The config to use for the Runnable. Defaults to None.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### astream_events

```python
astream_events(self, input: 'Any', config: 'Optional[RunnableConfig]' = None, version: "Literal['v1', 'v2']", include_names: 'Optional[Sequence[str]]' = None, include_types: 'Optional[Sequence[str]]' = None, include_tags: 'Optional[Sequence[str]]' = None, exclude_names: 'Optional[Sequence[str]]' = None, exclude_types: 'Optional[Sequence[str]]' = None, exclude_tags: 'Optional[Sequence[str]]' = None, **kwargs: 'Any')
```

Generate a stream of events.

        Use to create an iterator over StreamEvents that provide real-time information
        about the progress of the Runnable, including StreamEvents from intermediate
        results.

        A StreamEvent is a dictionary with the following schema:

        - ``event``: **str** - Event names are of the
            format: on_[runnable_type]_(start|stream|end).
        - ``name``: **str** - The name of the Runnable that generated the event.
        - ``run_id``: **str** - randomly generated ID associated with the given execution of
            the Runnable that emitted the event.
            A child Runnable that gets invoked as part of the execution of a
            parent Runnable is assigned its own unique ID.
        - ``parent_ids``: **List[str]** - The IDs of the parent runnables that
            generated the event. The root Runnable will have an empty list.
            The order of the parent IDs is from the root to the immediate parent.
            Only available for v2 version of the API. The v1 version of the API
            will return an empty list.
        - ``tags``: **Optional[List[str]]** - The tags of the Runnable that generated
            the event.
        - ``metadata``: **Optional[Dict[str, Any]]** - The metadata of the Runnable
            that generated the event.
        - ``data``: **Dict[str, Any]**


        Below is a table that illustrates some events that might be emitted by various
        chains. Metadata fields have been omitted from the table for brevity.
        Chain definitions have been included after the table.

        **ATTENTION** This reference table is for the V2 version of the schema.

        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | event                | name             | chunk                           | input                                         | output                                          |
        +======================+==================+=================================+===============================================+=================================================+
        | on_chat_model_start  | [model name]     |                                 | {"messages": [[SystemMessage, HumanMessage]]} |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chat_model_stream | [model name]     | AIMessageChunk(content="hello") |                                               |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chat_model_end    | [model name]     |                                 | {"messages": [[SystemMessage, HumanMessage]]} | AIMessageChunk(content="hello world")           |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_llm_start         | [model name]     |                                 | {'input': 'hello'}                            |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_llm_stream        | [model name]     | 'Hello'                         |                                               |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_llm_end           | [model name]     |                                 | 'Hello human!'                                |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chain_start       | format_docs      |                                 |                                               |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chain_stream      | format_docs      | "hello world!, goodbye world!"  |                                               |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_chain_end         | format_docs      |                                 | [Document(...)]                               | "hello world!, goodbye world!"                  |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_tool_start        | some_tool        |                                 | {"x": 1, "y": "2"}                            |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_tool_end          | some_tool        |                                 |                                               | {"x": 1, "y": "2"}                              |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_retriever_start   | [retriever name] |                                 | {"query": "hello"}                            |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_retriever_end     | [retriever name] |                                 | {"query": "hello"}                            | [Document(...), ..]                             |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_prompt_start      | [template_name]  |                                 | {"question": "hello"}                         |                                                 |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+
        | on_prompt_end        | [template_name]  |                                 | {"question": "hello"}                         | ChatPromptValue(messages: [SystemMessage, ...]) |
        +----------------------+------------------+---------------------------------+-----------------------------------------------+-------------------------------------------------+

        In addition to the standard events, users can also dispatch custom events (see example below).

        Custom events will be only be surfaced with in the `v2` version of the API!

        A custom event has following format:

        +-----------+------+-----------------------------------------------------------------------------------------------------------+
        | Attribute | Type | Description                                                                                               |
        +===========+======+===========================================================================================================+
        | name      | str  | A user defined name for the event.                                                                        |
        +-----------+------+-----------------------------------------------------------------------------------------------------------+
        | data      | Any  | The data associated with the event. This can be anything, though we suggest making it JSON serializable.  |
        +-----------+------+-----------------------------------------------------------------------------------------------------------+

        Here are declarations associated with the standard events shown above:

        `format_docs`:

        .. code-block:: python

            def format_docs(docs: List[Document]) -> str:
                '''Format the docs.'''
                return ", ".join([doc.page_content for doc in docs])

            format_docs = RunnableLambda(format_docs)

        `some_tool`:

        .. code-block:: python

            @tool
            def some_tool(x: int, y: str) -> dict:
                '''Some_tool.'''
                return {"x": x, "y": y}

        `prompt`:

        .. code-block:: python

            template = ChatPromptTemplate.from_messages(
                [("system", "You are Cat Agent 007"), ("human", "{question}")]
            ).with_config({"run_name": "my_template", "tags": ["my_template"]})


        Example:

        .. code-block:: python

            from langchain_core.runnables import RunnableLambda

            async def reverse(s: str) -> str:
                return s[::-1]

            chain = RunnableLambda(func=reverse)

            events = [
                event async for event in chain.astream_events("hello", version="v2")
            ]

            # will produce the following events (run_id, and parent_ids
            # has been omitted for brevity):
            [
                {
                    "data": {"input": "hello"},
                    "event": "on_chain_start",
                    "metadata": {},
                    "name": "reverse",
                    "tags": [],
                },
                {
                    "data": {"chunk": "olleh"},
                    "event": "on_chain_stream",
                    "metadata": {},
                    "name": "reverse",
                    "tags": [],
                },
                {
                    "data": {"output": "olleh"},
                    "event": "on_chain_end",
                    "metadata": {},
                    "name": "reverse",
                    "tags": [],
                },
            ]


        Example: Dispatch Custom Event

        .. code-block:: python

            from langchain_core.callbacks.manager import (
                adispatch_custom_event,
            )
            from langchain_core.runnables import RunnableLambda, RunnableConfig
            import asyncio


            async def slow_thing(some_input: str, config: RunnableConfig) -> str:
                """Do something that takes a long time."""
                await asyncio.sleep(1) # Placeholder for some slow operation
                await adispatch_custom_event(
                    "progress_event",
                    {"message": "Finished step 1 of 3"},
                    config=config # Must be included for python < 3.10
                )
                await asyncio.sleep(1) # Placeholder for some slow operation
                await adispatch_custom_event(
                    "progress_event",
                    {"message": "Finished step 2 of 3"},
                    config=config # Must be included for python < 3.10
                )
                await asyncio.sleep(1) # Placeholder for some slow operation
                return "Done"

            slow_thing = RunnableLambda(slow_thing)

            async for event in slow_thing.astream_events("some_input", version="v2"):
                print(event)

        Args:
            input: The input to the Runnable.
            config: The config to use for the Runnable.
            version: The version of the schema to use either `v2` or `v1`.
                     Users should use `v2`.
                     `v1` is for backwards compatibility and will be deprecated
                     in 0.4.0.
                     No default will be assigned until the API is stabilized.
                     custom events will only be surfaced in `v2`.
            include_names: Only include events from runnables with matching names.
            include_types: Only include events from runnables with matching types.
            include_tags: Only include events from runnables with matching tags.
            exclude_names: Exclude events from runnables with matching names.
            exclude_types: Exclude events from runnables with matching types.
            exclude_tags: Exclude events from runnables with matching tags.
            kwargs: Additional keyword arguments to pass to the Runnable.
                These will be passed to astream_log as this implementation
                of astream_events is built on top of astream_log.

        Yields:
            An async stream of StreamEvents.

        Raises:
            NotImplementedError: If the version is not `v1` or `v2`.

###### Parameters

- **input**: The input to the Runnable.
- **config**: RunnableConfig) -> str:
                """Do something that takes a long time."""
                await asyncio.sleep(1) # Placeholder for some slow operation
                await adispatch_custom_event(
                    "progress_event",
                    {"message": "Finished step 1 of 3"},
                    config=config # Must be included for python < 3.10
                )
                await asyncio.sleep(1) # Placeholder for some slow operation
                await adispatch_custom_event(
                    "progress_event",
                    {"message": "Finished step 2 of 3"},
                    config=config # Must be included for python < 3.10
                )
                await asyncio.sleep(1) # Placeholder for some slow operation
                return "Done"

            slow_thing = RunnableLambda(slow_thing)

            async for event in slow_thing.astream_events("some_input", version="v2"):
                print(event)
- **version**: The version of the schema to use either `v2` or `v1`.
                     Users should use `v2`.
                     `v1` is for backwards compatibility and will be deprecated
                     in 0.4.0.
                     No default will be assigned until the API is stabilized.
                     custom events will only be surfaced in `v2`.
- **include_names**: Only include events from runnables with matching names.
- **include_types**: Only include events from runnables with matching types.
- **include_tags**: Only include events from runnables with matching tags.
- **exclude_names**: Exclude events from runnables with matching names.
- **exclude_types**: Exclude events from runnables with matching types.
- **exclude_tags**: Exclude events from runnables with matching tags.
- **kwargs**: Additional keyword arguments to pass to the Runnable.
                These will be passed to astream_log as this implementation
                of astream_events is built on top of astream_log.

##### astream_log

```python
astream_log(self, input: 'Any', config: 'Optional[RunnableConfig]' = None, diff: 'bool' = True, with_streamed_output_list: 'bool' = True, include_names: 'Optional[Sequence[str]]' = None, include_types: 'Optional[Sequence[str]]' = None, include_tags: 'Optional[Sequence[str]]' = None, exclude_names: 'Optional[Sequence[str]]' = None, exclude_types: 'Optional[Sequence[str]]' = None, exclude_tags: 'Optional[Sequence[str]]' = None, **kwargs: 'Any')
```

Stream all output from a Runnable, as reported to the callback system.
        This includes all inner runs of LLMs, Retrievers, Tools, etc.

        Output is streamed as Log objects, which include a list of
        Jsonpatch ops that describe how the state of the run has changed in each
        step, and the final state of the run.

        The Jsonpatch ops can be applied in order to construct state.

        Args:
            input: The input to the Runnable.
            config: The config to use for the Runnable.
            diff: Whether to yield diffs between each step or the current state.
            with_streamed_output_list: Whether to yield the streamed_output list.
            include_names: Only include logs with these names.
            include_types: Only include logs with these types.
            include_tags: Only include logs with these tags.
            exclude_names: Exclude logs with these names.
            exclude_types: Exclude logs with these types.
            exclude_tags: Exclude logs with these tags.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            A RunLogPatch or RunLog object.

###### Parameters

- **input**: The input to the Runnable.
- **config**: The config to use for the Runnable.
- **diff**: Whether to yield diffs between each step or the current state.
- **with_streamed_output_list**: Whether to yield the streamed_output list.
- **include_names**: Only include logs with these names.
- **include_types**: Only include logs with these types.
- **include_tags**: Only include logs with these tags.
- **exclude_names**: Exclude logs with these names.
- **exclude_types**: Exclude logs with these types.
- **exclude_tags**: Exclude logs with these tags.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### atransform

```python
atransform(self, input: 'AsyncIterator[Input]', config: 'Optional[RunnableConfig]' = None, **kwargs: 'Optional[Any]')
```

Default implementation of atransform, which buffers input and calls astream.
        Subclasses should override this method if they can start producing output while
        input is still being generated.

        Args:
            input: An async iterator of inputs to the Runnable.
            config: The config to use for the Runnable. Defaults to None.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            The output of the Runnable.

###### Parameters

- **input**: An async iterator of inputs to the Runnable.
- **config**: The config to use for the Runnable. Defaults to None.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### batch

```python
batch(self, inputs: 'list[Input]', config: 'Optional[Union[RunnableConfig, list[RunnableConfig]]]' = None, return_exceptions: 'bool' = False, **kwargs: 'Optional[Any]')
```

Default implementation runs invoke in parallel using a thread pool executor.

        The default implementation of batch works well for IO bound runnables.

        Subclasses should override this method if they can batch more efficiently;
        e.g., if the underlying Runnable uses an API which supports a batch mode.

##### batch_as_completed

```python
batch_as_completed(self, inputs: 'Sequence[Input]', config: 'Optional[Union[RunnableConfig, Sequence[RunnableConfig]]]' = None, return_exceptions: 'bool' = False, **kwargs: 'Optional[Any]')
```

Run invoke in parallel on a list of inputs,
        yielding results as they complete.

##### bind

```python
bind(self, **kwargs: 'Any')
```

Bind arguments to a Runnable, returning a new Runnable.

        Useful when a Runnable in a chain requires an argument that is not
        in the output of the previous Runnable or included in the user input.

        Args:
            kwargs: The arguments to bind to the Runnable.

        Returns:
            A new Runnable with the arguments bound.

        Example:

        .. code-block:: python

            from langchain_community.chat_models import ChatOllama
            from langchain_core.output_parsers import StrOutputParser

            llm = ChatOllama(model='llama2')

            # Without bind.
            chain = (
                llm
                | StrOutputParser()
            )

            chain.invoke("Repeat quoted words exactly: 'One two three four five.'")
            # Output is 'One two three four five.'

            # With bind.
            chain = (
                llm.bind(stop=["three"])
                | StrOutputParser()
            )

            chain.invoke("Repeat quoted words exactly: 'One two three four five.'")
            # Output is 'One two'

###### Parameters

- **kwargs**: The arguments to bind to the Runnable.

###### Returns

A new Runnable with the arguments bound.

##### config_schema

```python
config_schema(self, include: 'Optional[Sequence[str]]' = None)
```

The type of config this Runnable accepts specified as a pydantic model.

        To mark a field as configurable, see the `configurable_fields`
        and `configurable_alternatives` methods.

        Args:
            include: A list of fields to include in the config schema.

        Returns:
            A pydantic model that can be used to validate config.

###### Parameters

- **include**: A list of fields to include in the config schema.

###### Returns

A pydantic model that can be used to validate config.

##### configurable_alternatives

```python
configurable_alternatives(self, which: 'ConfigurableField', default_key: 'str' = 'default', prefix_keys: 'bool' = False, **kwargs: 'Union[Runnable[Input, Output], Callable[[], Runnable[Input, Output]]]')
```

Configure alternatives for Runnables that can be set at runtime.

        Args:
            which: The ConfigurableField instance that will be used to select the
                alternative.
            default_key: The default key to use if no alternative is selected.
                Defaults to "default".
            prefix_keys: Whether to prefix the keys with the ConfigurableField id.
                Defaults to False.
            **kwargs: A dictionary of keys to Runnable instances or callables that
                return Runnable instances.

        Returns:
            A new Runnable with the alternatives configured.

        .. code-block:: python

            from langchain_anthropic import ChatAnthropic
            from langchain_core.runnables.utils import ConfigurableField
            from langchain_openai import ChatOpenAI

            model = ChatAnthropic(
                model_name="claude-3-sonnet-20240229"
            ).configurable_alternatives(
                ConfigurableField(id="llm"),
                default_key="anthropic",
                openai=ChatOpenAI()
            )

            # uses the default model ChatAnthropic
            print(model.invoke("which organization created you?").content)

            # uses ChatOpenAI
            print(
                model.with_config(
                    configurable={"llm": "openai"}
                ).invoke("which organization created you?").content
            )

###### Parameters

- **which**: The ConfigurableField instance that will be used to select the
                alternative.
- **default_key**: The default key to use if no alternative is selected.
                Defaults to "default".
- **prefix_keys**: Whether to prefix the keys with the ConfigurableField id.
                Defaults to False.
            **kwargs: A dictionary of keys to Runnable instances or callables that
                return Runnable instances.

###### Returns

A new Runnable with the alternatives configured.

        .. code-block:: python

            from langchain_anthropic import ChatAnthropic
            from langchain_core.runnables.utils import ConfigurableField
            from langchain_openai import ChatOpenAI

            model = ChatAnthropic(
                model_name="claude-3-sonnet-20240229"
            ).configurable_alternatives(
                ConfigurableField(id="llm"),
                default_key="anthropic",
                openai=ChatOpenAI()
            )

            # uses the default model ChatAnthropic
            print(model.invoke("which organization created you?").content)

            # uses ChatOpenAI
            print(
                model.with_config(
                    configurable={"llm": "openai"}
                ).invoke("which organization created you?").content
            )

##### configurable_fields

```python
configurable_fields(self, **kwargs: 'AnyConfigurableField')
```

Configure particular Runnable fields at runtime.

        Args:
            **kwargs: A dictionary of ConfigurableField instances to configure.

        Returns:
            A new Runnable with the fields configured.

        .. code-block:: python

            from langchain_core.runnables import ConfigurableField
            from langchain_openai import ChatOpenAI

            model = ChatOpenAI(max_tokens=20).configurable_fields(
                max_tokens=ConfigurableField(
                    id="output_token_number",
                    name="Max tokens in the output",
                    description="The maximum number of tokens in the output",
                )
            )

            # max_tokens = 20
            print(
                "max_tokens_20: ",
                model.invoke("tell me something about chess").content
            )

            # max_tokens = 200
            print("max_tokens_200: ", model.with_config(
                configurable={"output_token_number": 200}
                ).invoke("tell me something about chess").content
            )

###### Parameters


###### Returns

A new Runnable with the fields configured.

        .. code-block:: python

            from langchain_core.runnables import ConfigurableField
            from langchain_openai import ChatOpenAI

            model = ChatOpenAI(max_tokens=20).configurable_fields(
                max_tokens=ConfigurableField(
                    id="output_token_number",
                    name="Max tokens in the output",
                    description="The maximum number of tokens in the output",
                )
            )

            # max_tokens = 20
            print(
                "max_tokens_20: ",
                model.invoke("tell me something about chess").content
            )

            # max_tokens = 200
            print("max_tokens_200: ", model.with_config(
                configurable={"output_token_number": 200}
                ).invoke("tell me something about chess").content
            )

##### copy

```python
copy(self, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False)
```

Returns a copy of the model.

        !!! warning "Deprecated"
            This method is now deprecated; use `model_copy` instead.

        If you need `include` or `exclude`, use:

        ```python {test="skip" lint="skip"}
        data = self.model_dump(include=include, exclude=exclude, round_trip=True)
        data = {**data, **(update or {})}
        copied = self.model_validate(data)
        ```

        Args:
            include: Optional set or mapping specifying which fields to include in the copied model.
            exclude: Optional set or mapping specifying which fields to exclude in the copied model.
            update: Optional dictionary of field-value pairs to override field values in the copied model.
            deep: If True, the values of fields that are Pydantic models will be deep-copied.

        Returns:
            A copy of the model with included, excluded and updated fields as specified.

###### Parameters

- **include**: Optional set or mapping specifying which fields to include in the copied model.
- **exclude**: Optional set or mapping specifying which fields to exclude in the copied model.
- **update**: Optional dictionary of field-value pairs to override field values in the copied model.
- **deep**: If True, the values of fields that are Pydantic models will be deep-copied.

###### Returns

A copy of the model with included, excluded and updated fields as specified.

##### dict

```python
dict(self, **kwargs: 'Any')
```

Return dictionary representation of prompt.

        Args:
            kwargs: Any additional arguments to pass to the dictionary.

        Returns:
            Dict: Dictionary representation of the prompt.

        Raises:
            NotImplementedError: If the prompt type is not implemented.

###### Parameters

- **kwargs**: Any additional arguments to pass to the dictionary.

###### Returns



##### format

```python
format(self, **kwargs: 'Any')
```

Format the prompt with the inputs.

        Args:
            kwargs: Any arguments to be passed to the prompt template.

        Returns:
            A formatted string.

###### Parameters

- **kwargs**: Any arguments to be passed to the prompt template.

###### Returns

A formatted string.

##### format_prompt

```python
format_prompt(self, **kwargs: 'Any')
```

Format the prompt with the inputs.

        Args:
            kwargs: Any arguments to be passed to the prompt template.

        Returns:
            A formatted string.

###### Parameters

- **kwargs**: Any arguments to be passed to the prompt template.

###### Returns

A formatted string.

##### get_config_jsonschema

```python
get_config_jsonschema(self, include: 'Optional[Sequence[str]]' = None)
```

Get a JSON schema that represents the config of the Runnable.

        Args:
            include: A list of fields to include in the config schema.

        Returns:
            A JSON schema that represents the config of the Runnable.

        .. versionadded:: 0.3.0

###### Parameters

- **include**: A list of fields to include in the config schema.

###### Returns

A JSON schema that represents the config of the Runnable.

        .. versionadded:: 0.3.0

##### get_graph

```python
get_graph(self, config: 'Optional[RunnableConfig]' = None)
```

Return a graph representation of this Runnable.

##### get_input_jsonschema

```python
get_input_jsonschema(self, config: 'Optional[RunnableConfig]' = None)
```

Get a JSON schema that represents the input to the Runnable.

        Args:
            config: A config to use when generating the schema.

        Returns:
            A JSON schema that represents the input to the Runnable.

        Example:

            .. code-block:: python

                from langchain_core.runnables import RunnableLambda

                def add_one(x: int) -> int:
                    return x + 1

                runnable = RunnableLambda(add_one)

                print(runnable.get_input_jsonschema())

        .. versionadded:: 0.3.0

###### Parameters

- **config**: A config to use when generating the schema.

###### Returns

A JSON schema that represents the input to the Runnable.

##### get_input_schema

```python
get_input_schema(self, config: 'RunnableConfig | None' = None)
```

Get the input schema for the prompt.

        Args:
            config: The runnable configuration.

        Returns:
            The input schema for the prompt.

###### Parameters

- **config**: The runnable configuration.

###### Returns

The input schema for the prompt.

##### get_name

```python
get_name(self, suffix: 'Optional[str]' = None, name: 'Optional[str]' = None)
```

Get the name of the Runnable.

##### get_output_jsonschema

```python
get_output_jsonschema(self, config: 'Optional[RunnableConfig]' = None)
```

Get a JSON schema that represents the output of the Runnable.

        Args:
            config: A config to use when generating the schema.

        Returns:
            A JSON schema that represents the output of the Runnable.

        Example:

            .. code-block:: python

                from langchain_core.runnables import RunnableLambda

                def add_one(x: int) -> int:
                    return x + 1

                runnable = RunnableLambda(add_one)

                print(runnable.get_output_jsonschema())

        .. versionadded:: 0.3.0

###### Parameters

- **config**: A config to use when generating the schema.

###### Returns

A JSON schema that represents the output of the Runnable.

##### get_output_schema

```python
get_output_schema(self, config: 'Optional[RunnableConfig]' = None)
```

Get a pydantic model that can be used to validate output to the Runnable.

        Runnables that leverage the configurable_fields and configurable_alternatives
        methods will have a dynamic output schema that depends on which
        configuration the Runnable is invoked with.

        This method allows to get an output schema for a specific configuration.

        Args:
            config: A config to use when generating the schema.

        Returns:
            A pydantic model that can be used to validate output.

###### Parameters

- **config**: A config to use when generating the schema.

###### Returns

A pydantic model that can be used to validate output.

##### get_prompts

```python
get_prompts(self, config: 'Optional[RunnableConfig]' = None)
```

Return a list of prompts used by this Runnable.

##### invoke

```python
invoke(self, input: 'dict', config: 'Optional[RunnableConfig]' = None, **kwargs: 'Any')
```

Invoke the prompt.

        Args:
            input: Dict, input to the prompt.
            config: RunnableConfig, configuration for the prompt.

        Returns:
            PromptValue: The output of the prompt.

###### Parameters

- **input**: Dict, input to the prompt.
- **config**: RunnableConfig, configuration for the prompt.

###### Returns



##### json

```python
json(self, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any')
```

##### map

```python
map(self)
```

Return a new Runnable that maps a list of inputs to a list of outputs,
        by calling invoke() with each input.

        Returns:
            A new Runnable that maps a list of inputs to a list of outputs.

        Example:

            .. code-block:: python

                    from langchain_core.runnables import RunnableLambda

                    def _lambda(x: int) -> int:
                        return x + 1

                    runnable = RunnableLambda(_lambda)
                    print(runnable.map().invoke([1, 2, 3])) # [2, 3, 4]

###### Returns

A new Runnable that maps a list of inputs to a list of outputs.

##### model_copy

```python
model_copy(self, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False)
```

Usage docs: https://docs.pydantic.dev/2.10/concepts/serialization/#model_copy

        Returns a copy of the model.

        Args:
            update: Values to change/add in the new model. Note: the data is not validated
                before creating the new model. You should trust this data.
            deep: Set to `True` to make a deep copy of the model.

        Returns:
            New model instance.

###### Parameters

- **update**: Values to change/add in the new model. Note: the data is not validated
                before creating the new model. You should trust this data.
- **deep**: Set to `True` to make a deep copy of the model.

###### Returns

New model instance.

##### model_dump

```python
model_dump(self, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, serialize_as_any: 'bool' = False)
```

Usage docs: https://docs.pydantic.dev/2.10/concepts/serialization/#modelmodel_dump

        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        Args:
            mode: The mode in which `to_python` should run.
                If mode is 'json', the output will only contain JSON serializable types.
                If mode is 'python', the output may contain non-JSON-serializable Python objects.
            include: A set of fields to include in the output.
            exclude: A set of fields to exclude from the output.
            context: Additional context to pass to the serializer.
            by_alias: Whether to use the field's alias in the dictionary key if defined.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of `None`.
            round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
            warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
            serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

        Returns:
            A dictionary representation of the model.

###### Parameters

- **mode**: The mode in which `to_python` should run.
                If mode is 'json', the output will only contain JSON serializable types.
                If mode is 'python', the output may contain non-JSON-serializable Python objects.
- **include**: A set of fields to include in the output.
- **exclude**: A set of fields to exclude from the output.
- **context**: Additional context to pass to the serializer.
- **by_alias**: Whether to use the field's alias in the dictionary key if defined.
- **exclude_unset**: Whether to exclude fields that have not been explicitly set.
- **exclude_defaults**: Whether to exclude fields that are set to their default value.
- **exclude_none**: Whether to exclude fields that have a value of `None`.
- **round_trip**: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- **warnings**: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- **serialize_as_any**: Whether to serialize fields with duck-typing serialization behavior.

###### Returns

A dictionary representation of the model.

##### model_dump_json

```python
model_dump_json(self, indent: 'int | None' = None, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, serialize_as_any: 'bool' = False)
```

Usage docs: https://docs.pydantic.dev/2.10/concepts/serialization/#modelmodel_dump_json

        Generates a JSON representation of the model using Pydantic's `to_json` method.

        Args:
            indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
            include: Field(s) to include in the JSON output.
            exclude: Field(s) to exclude from the JSON output.
            context: Additional context to pass to the serializer.
            by_alias: Whether to serialize using field aliases.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of `None`.
            round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
            warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
            serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

        Returns:
            A JSON string representation of the model.

###### Parameters

- **indent**: Indentation to use in the JSON output. If None is passed, the output will be compact.
- **include**: Field(s) to include in the JSON output.
- **exclude**: Field(s) to exclude from the JSON output.
- **context**: Additional context to pass to the serializer.
- **by_alias**: Whether to serialize using field aliases.
- **exclude_unset**: Whether to exclude fields that have not been explicitly set.
- **exclude_defaults**: Whether to exclude fields that are set to their default value.
- **exclude_none**: Whether to exclude fields that have a value of `None`.
- **round_trip**: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- **warnings**: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- **serialize_as_any**: Whether to serialize fields with duck-typing serialization behavior.

###### Returns

A JSON string representation of the model.

##### model_post_init

```python
model_post_init(self, _BaseModel__context: 'Any')
```

Override this method to perform additional initialization after `__init__` and `model_construct`.
        This is useful if you want to do some validation that requires the entire model to be initialized.

##### partial

```python
partial(self, **kwargs: 'Union[str, Callable[[], str]]')
```

Return a partial of the prompt template.

        Args:
            kwargs: Union[str, Callable[[], str]], partial variables to set.

        Returns:
            BasePromptTemplate: A partial of the prompt template.

###### Parameters

- **kwargs**: Union[str, Callable[[], str]], partial variables to set.

###### Returns



##### pick

```python
pick(self, keys: 'Union[str, list[str]]')
```

Pick keys from the output dict of this Runnable.

        Pick single key:
            .. code-block:: python

                import json

                from langchain_core.runnables import RunnableLambda, RunnableMap

                as_str = RunnableLambda(str)
                as_json = RunnableLambda(json.loads)
                chain = RunnableMap(str=as_str, json=as_json)

                chain.invoke("[1, 2, 3]")
                # -> {"str": "[1, 2, 3]", "json": [1, 2, 3]}

                json_only_chain = chain.pick("json")
                json_only_chain.invoke("[1, 2, 3]")
                # -> [1, 2, 3]

        Pick list of keys:
            .. code-block:: python

                from typing import Any

                import json

                from langchain_core.runnables import RunnableLambda, RunnableMap

                as_str = RunnableLambda(str)
                as_json = RunnableLambda(json.loads)
                def as_bytes(x: Any) -> bytes:
                    return bytes(x, "utf-8")

                chain = RunnableMap(
                    str=as_str,
                    json=as_json,
                    bytes=RunnableLambda(as_bytes)
                )

                chain.invoke("[1, 2, 3]")
                # -> {"str": "[1, 2, 3]", "json": [1, 2, 3], "bytes": b"[1, 2, 3]"}

                json_and_bytes_chain = chain.pick(["json", "bytes"])
                json_and_bytes_chain.invoke("[1, 2, 3]")
                # -> {"json": [1, 2, 3], "bytes": b"[1, 2, 3]"}

##### pipe

```python
pipe(self, *others: 'Union[Runnable[Any, Other], Callable[[Any], Other]]', name: 'Optional[str]' = None)
```

Compose this Runnable with Runnable-like objects to make a RunnableSequence.

        Equivalent to `RunnableSequence(self, *others)` or `self | others[0] | ...`

        Example:
            .. code-block:: python

                from langchain_core.runnables import RunnableLambda

                def add_one(x: int) -> int:
                    return x + 1

                def mul_two(x: int) -> int:
                    return x * 2

                runnable_1 = RunnableLambda(add_one)
                runnable_2 = RunnableLambda(mul_two)
                sequence = runnable_1.pipe(runnable_2)
                # Or equivalently:
                # sequence = runnable_1 | runnable_2
                # sequence = RunnableSequence(first=runnable_1, last=runnable_2)
                sequence.invoke(1)
                await sequence.ainvoke(1)
                # -> 4

                sequence.batch([1, 2, 3])
                await sequence.abatch([1, 2, 3])
                # -> [4, 6, 8]

##### pretty_print

```python
pretty_print(self)
```

Print a pretty representation of the prompt.

##### pretty_repr

```python
pretty_repr(self, html: 'bool' = False)
```

Get a pretty representation of the prompt.

        Args:
            html: Whether to return an HTML-formatted string.

        Returns:
            A pretty representation of the prompt.

###### Parameters

- **html**: Whether to return an HTML-formatted string.

###### Returns

A pretty representation of the prompt.

##### save

```python
save(self, file_path: 'Union[Path, str]')
```

Save the prompt.

        Args:
            file_path: Path to directory to save prompt to.

        Raises:
            ValueError: If the prompt has partial variables.
            ValueError: If the file path is not json or yaml.
            NotImplementedError: If the prompt type is not implemented.

        Example:
        .. code-block:: python

            prompt.save(file_path="path/prompt.yaml")

###### Parameters

- **file_path**: Path to directory to save prompt to.

##### stream

```python
stream(self, input: 'Input', config: 'Optional[RunnableConfig]' = None, **kwargs: 'Optional[Any]')
```

Default implementation of stream, which calls invoke.
        Subclasses should override this method if they support streaming output.

        Args:
            input: The input to the Runnable.
            config: The config to use for the Runnable. Defaults to None.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            The output of the Runnable.

###### Parameters

- **input**: The input to the Runnable.
- **config**: The config to use for the Runnable. Defaults to None.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### to_json

```python
to_json(self)
```

Serialize the Runnable to JSON.

        Returns:
            A JSON-serializable representation of the Runnable.

###### Returns

A JSON-serializable representation of the Runnable.

##### to_json_not_implemented

```python
to_json_not_implemented(self)
```

##### transform

```python
transform(self, input: 'Iterator[Input]', config: 'Optional[RunnableConfig]' = None, **kwargs: 'Optional[Any]')
```

Default implementation of transform, which buffers input and calls astream.

        Subclasses should override this method if they can start producing output while
        input is still being generated.

        Args:
            input: An iterator of inputs to the Runnable.
            config: The config to use for the Runnable. Defaults to None.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Yields:
            The output of the Runnable.

###### Parameters

- **input**: An iterator of inputs to the Runnable.
- **config**: The config to use for the Runnable. Defaults to None.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

##### validate_variable_names

```python
validate_variable_names(self)
```

Validate variable names do not include restricted names.

##### with_alisteners

```python
with_alisteners(self, on_start: 'Optional[AsyncListener]' = None, on_end: 'Optional[AsyncListener]' = None, on_error: 'Optional[AsyncListener]' = None)
```

Bind async lifecycle listeners to a Runnable, returning a new Runnable.

        on_start: Asynchronously called before the Runnable starts running.
        on_end: Asynchronously called after the Runnable finishes running.
        on_error: Asynchronously called if the Runnable throws an error.

        The Run object contains information about the run, including its id,
        type, input, output, error, start_time, end_time, and any tags or metadata
        added to the run.

        Args:
            on_start: Asynchronously called before the Runnable starts running.
                Defaults to None.
            on_end: Asynchronously called after the Runnable finishes running.
                Defaults to None.
            on_error: Asynchronously called if the Runnable throws an error.
                Defaults to None.

        Returns:
            A new Runnable with the listeners bound.

        Example:

        .. code-block:: python

            from langchain_core.runnables import RunnableLambda
            import time

            async def test_runnable(time_to_sleep : int):
                print(f"Runnable[{time_to_sleep}s]: starts at {format_t(time.time())}")
                await asyncio.sleep(time_to_sleep)
                print(f"Runnable[{time_to_sleep}s]: ends at {format_t(time.time())}")

            async def fn_start(run_obj : Runnable):
                print(f"on start callback starts at {format_t(time.time())}
                await asyncio.sleep(3)
                print(f"on start callback ends at {format_t(time.time())}")

            async def fn_end(run_obj : Runnable):
                print(f"on end callback starts at {format_t(time.time())}
                await asyncio.sleep(2)
                print(f"on end callback ends at {format_t(time.time())}")

            runnable = RunnableLambda(test_runnable).with_alisteners(
                on_start=fn_start,
                on_end=fn_end
            )
            async def concurrent_runs():
                await asyncio.gather(runnable.ainvoke(2), runnable.ainvoke(3))

            asyncio.run(concurrent_runs())
            Result:
            on start callback starts at 2024-05-16T14:20:29.637053+00:00
            on start callback starts at 2024-05-16T14:20:29.637150+00:00
            on start callback ends at 2024-05-16T14:20:32.638305+00:00
            on start callback ends at 2024-05-16T14:20:32.638383+00:00
            Runnable[3s]: starts at 2024-05-16T14:20:32.638849+00:00
            Runnable[5s]: starts at 2024-05-16T14:20:32.638999+00:00
            Runnable[3s]: ends at 2024-05-16T14:20:35.640016+00:00
            on end callback starts at 2024-05-16T14:20:35.640534+00:00
            Runnable[5s]: ends at 2024-05-16T14:20:37.640169+00:00
            on end callback starts at 2024-05-16T14:20:37.640574+00:00
            on end callback ends at 2024-05-16T14:20:37.640654+00:00
            on end callback ends at 2024-05-16T14:20:39.641751+00:00

###### Parameters

- **on_start**: Asynchronously called before the Runnable starts running.
- **on_end**: Asynchronously called after the Runnable finishes running.
- **on_error**: Asynchronously called if the Runnable throws an error.

        The Run object contains information about the run, including its id,
        type, input, output, error, start_time, end_time, and any tags or metadata
        added to the run.

###### Returns

A new Runnable with the listeners bound.

##### with_config

```python
with_config(self, config: 'Optional[RunnableConfig]' = None, **kwargs: 'Any')
```

Bind config to a Runnable, returning a new Runnable.

        Args:
            config: The config to bind to the Runnable.
            kwargs: Additional keyword arguments to pass to the Runnable.

        Returns:
            A new Runnable with the config bound.

###### Parameters

- **config**: The config to bind to the Runnable.
- **kwargs**: Additional keyword arguments to pass to the Runnable.

###### Returns

A new Runnable with the config bound.

##### with_fallbacks

```python
with_fallbacks(self, fallbacks: 'Sequence[Runnable[Input, Output]]', exceptions_to_handle: 'tuple[type[BaseException], ...]' = (<class 'Exception'>,), exception_key: 'Optional[str]' = None)
```

Add fallbacks to a Runnable, returning a new Runnable.

        The new Runnable will try the original Runnable, and then each fallback
        in order, upon failures.

        Args:
            fallbacks: A sequence of runnables to try if the original Runnable fails.
            exceptions_to_handle: A tuple of exception types to handle.
                Defaults to (Exception,).
            exception_key: If string is specified then handled exceptions will be passed
                to fallbacks as part of the input under the specified key. If None,
                exceptions will not be passed to fallbacks. If used, the base Runnable
                and its fallbacks must accept a dictionary as input. Defaults to None.

        Returns:
            A new Runnable that will try the original Runnable, and then each
            fallback in order, upon failures.

        Example:

            .. code-block:: python

                from typing import Iterator

                from langchain_core.runnables import RunnableGenerator


                def _generate_immediate_error(input: Iterator) -> Iterator[str]:
                    raise ValueError()
                    yield ""


                def _generate(input: Iterator) -> Iterator[str]:
                    yield from "foo bar"


                runnable = RunnableGenerator(_generate_immediate_error).with_fallbacks(
                    [RunnableGenerator(_generate)]
                    )
                print(''.join(runnable.stream({}))) #foo bar

        Args:
            fallbacks: A sequence of runnables to try if the original Runnable fails.
            exceptions_to_handle: A tuple of exception types to handle.
            exception_key: If string is specified then handled exceptions will be passed
                to fallbacks as part of the input under the specified key. If None,
                exceptions will not be passed to fallbacks. If used, the base Runnable
                and its fallbacks must accept a dictionary as input.

        Returns:
            A new Runnable that will try the original Runnable, and then each
            fallback in order, upon failures.

###### Parameters

- **fallbacks**: A sequence of runnables to try if the original Runnable fails.
- **exceptions_to_handle**: A tuple of exception types to handle.
                Defaults to (Exception,).
- **exception_key**: If string is specified then handled exceptions will be passed
                to fallbacks as part of the input under the specified key. If None,
                exceptions will not be passed to fallbacks. If used, the base Runnable
                and its fallbacks must accept a dictionary as input. Defaults to None.

###### Returns

A new Runnable that will try the original Runnable, and then each
            fallback in order, upon failures.

##### with_listeners

```python
with_listeners(self, on_start: 'Optional[Union[Callable[[Run], None], Callable[[Run, RunnableConfig], None]]]' = None, on_end: 'Optional[Union[Callable[[Run], None], Callable[[Run, RunnableConfig], None]]]' = None, on_error: 'Optional[Union[Callable[[Run], None], Callable[[Run, RunnableConfig], None]]]' = None)
```

Bind lifecycle listeners to a Runnable, returning a new Runnable.

        on_start: Called before the Runnable starts running, with the Run object.
        on_end: Called after the Runnable finishes running, with the Run object.
        on_error: Called if the Runnable throws an error, with the Run object.

        The Run object contains information about the run, including its id,
        type, input, output, error, start_time, end_time, and any tags or metadata
        added to the run.

        Args:
            on_start: Called before the Runnable starts running. Defaults to None.
            on_end: Called after the Runnable finishes running. Defaults to None.
            on_error: Called if the Runnable throws an error. Defaults to None.

        Returns:
            A new Runnable with the listeners bound.

        Example:

        .. code-block:: python

            from langchain_core.runnables import RunnableLambda
            from langchain_core.tracers.schemas import Run

            import time

            def test_runnable(time_to_sleep : int):
                time.sleep(time_to_sleep)

            def fn_start(run_obj: Run):
                print("start_time:", run_obj.start_time)

            def fn_end(run_obj: Run):
                print("end_time:", run_obj.end_time)

            chain = RunnableLambda(test_runnable).with_listeners(
                on_start=fn_start,
                on_end=fn_end
            )
            chain.invoke(2)

###### Parameters

- **on_start**: Called before the Runnable starts running, with the Run object.
- **on_end**: Called after the Runnable finishes running, with the Run object.
- **on_error**: Called if the Runnable throws an error, with the Run object.

        The Run object contains information about the run, including its id,
        type, input, output, error, start_time, end_time, and any tags or metadata
        added to the run.

###### Returns

A new Runnable with the listeners bound.

##### with_retry

```python
with_retry(self, retry_if_exception_type: 'tuple[type[BaseException], ...]' = (<class 'Exception'>,), wait_exponential_jitter: 'bool' = True, stop_after_attempt: 'int' = 3)
```

Create a new Runnable that retries the original Runnable on exceptions.

        Args:
            retry_if_exception_type: A tuple of exception types to retry on.
                Defaults to (Exception,).
            wait_exponential_jitter: Whether to add jitter to the wait
                time between retries. Defaults to True.
            stop_after_attempt: The maximum number of attempts to make before
                giving up. Defaults to 3.

        Returns:
            A new Runnable that retries the original Runnable on exceptions.

        Example:

        .. code-block:: python

            from langchain_core.runnables import RunnableLambda

            count = 0


            def _lambda(x: int) -> None:
                global count
                count = count + 1
                if x == 1:
                    raise ValueError("x is 1")
                else:
                     pass


            runnable = RunnableLambda(_lambda)
            try:
                runnable.with_retry(
                    stop_after_attempt=2,
                    retry_if_exception_type=(ValueError,),
                ).invoke(1)
            except ValueError:
                pass

            assert (count == 2)


        Args:
            retry_if_exception_type: A tuple of exception types to retry on
            wait_exponential_jitter: Whether to add jitter to the wait time
                                     between retries
            stop_after_attempt: The maximum number of attempts to make before giving up

        Returns:
            A new Runnable that retries the original Runnable on exceptions.

###### Parameters

- **retry_if_exception_type**: A tuple of exception types to retry on.
                Defaults to (Exception,).
- **wait_exponential_jitter**: Whether to add jitter to the wait
                time between retries. Defaults to True.
- **stop_after_attempt**: The maximum number of attempts to make before
                giving up. Defaults to 3.

###### Returns

A new Runnable that retries the original Runnable on exceptions.

##### with_types

```python
with_types(self, input_type: 'Optional[type[Input]]' = None, output_type: 'Optional[type[Output]]' = None)
```

Bind input and output types to a Runnable, returning a new Runnable.

        Args:
            input_type: The input type to bind to the Runnable. Defaults to None.
            output_type: The output type to bind to the Runnable. Defaults to None.

        Returns:
            A new Runnable with the types bound.

###### Parameters

- **input_type**: The input type to bind to the Runnable. Defaults to None.
- **output_type**: The output type to bind to the Runnable. Defaults to None.

###### Returns

A new Runnable with the types bound.

## Functions

### analyze_code_chunks

```python
analyze_code_chunks(file_path)
```

Analyze each code chunk using the LLM and collect suggestions.

### generate_roadmap_md

```python
generate_roadmap_md()
```

Generate a markdown file with the AGI/ASI roadmap.

### get_code_chunks

```python
get_code_chunks(file_path)
```

Extract code chunks (functions, classes) from a Python file.

### main

```python
main()
```

Main function to analyze specified Python files and generate roadmap.

