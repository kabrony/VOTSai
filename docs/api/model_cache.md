# model_cache

## Classes

### Any

Special type indicating an unconstrained type.

    - Any is compatible with every type.
    - Any assumed to have all methods.
    - All values assumed to be instances of Any.

    Note that all the above statements are true from the point of view of
    static type checkers. At runtime, Any should not be used with instance
    checks.

### ModelCache

Singleton cache for AI models to prevent redundant initialization.

#### Methods

##### clean_cache

```python
clean_cache(self, force: bool = False)
```

Clean up unused models to free memory.

##### clear_cache

```python
clear_cache(self)
```

Clear all models from the cache.

##### get_cache_info

```python
get_cache_info(self)
```

Get information about cached models.

##### get_model

```python
get_model(self, model_name: str, factory_func, *args, **kwargs)
```

Get a model from cache or create if not exists.

##### remove_model

```python
remove_model(self, name: str)
```

Remove a model from the cache.

