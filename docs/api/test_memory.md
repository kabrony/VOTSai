# test_memory

## Classes

### TestMemory

#### Methods

##### __init__

```python
__init__(self, methodName='runTest')
```

Create an instance of the class that will use the named test
           method when executed. Raises a ValueError if the instance does
           not have a method with the specified name.

##### addCleanup

```python
addCleanup(self, function, *args, **kwargs)
```

Add a function, with arguments, to be called when the test is
        completed. Functions added are called on a LIFO basis and are
        called after tearDown on test failure or success.

        Cleanup items are called even if setUp fails (unlike tearDown).

##### addTypeEqualityFunc

```python
addTypeEqualityFunc(self, typeobj, function)
```

Add a type specific assertEqual style function to compare a type.

        This method is for use by TestCase subclasses that need to register
        their own type equality functions to provide nicer error messages.

        Args:
            typeobj: The data type to call this function on when both values
                    are of the same type in assertEqual().
            function: The callable taking two arguments and an optional
                    msg= argument that raises self.failureException with a
                    useful error message when the two arguments are not equal.

###### Parameters

- **typeobj**: The data type to call this function on when both values
                    are of the same type in assertEqual().
- **function**: The callable taking two arguments and an optional
                    msg= argument that raises self.failureException with a
                    useful error message when the two arguments are not equal.

##### assertAlmostEqual

```python
assertAlmostEqual(self, first, second, places=None, msg=None, delta=None)
```

Fail if the two objects are unequal as determined by their
           difference rounded to the given number of decimal places
           (default 7) and comparing to zero, or by comparing that the
           difference between the two objects is more than the given
           delta.

           Note that decimal places (from zero) are usually not the same
           as significant digits (measured from the most significant digit).

           If the two objects compare equal then they will automatically
           compare almost equal.

##### assertCountEqual

```python
assertCountEqual(self, first, second, msg=None)
```

Asserts that two iterables have the same elements, the same number of
        times, without regard to order.

            self.assertEqual(Counter(list(first)),
                             Counter(list(second)))

         Example:
            - [0, 1, 1] and [1, 0, 1] compare equal.
            - [0, 0, 1] and [0, 1] compare unequal.

##### assertDictEqual

```python
assertDictEqual(self, d1, d2, msg=None)
```

##### assertEqual

```python
assertEqual(self, first, second, msg=None)
```

Fail if the two objects are unequal as determined by the '=='
           operator.

##### assertFalse

```python
assertFalse(self, expr, msg=None)
```

Check that the expression is false.

##### assertGreater

```python
assertGreater(self, a, b, msg=None)
```

Just like self.assertTrue(a > b), but with a nicer default message.

##### assertGreaterEqual

```python
assertGreaterEqual(self, a, b, msg=None)
```

Just like self.assertTrue(a >= b), but with a nicer default message.

##### assertIn

```python
assertIn(self, member, container, msg=None)
```

Just like self.assertTrue(a in b), but with a nicer default message.

##### assertIs

```python
assertIs(self, expr1, expr2, msg=None)
```

Just like self.assertTrue(a is b), but with a nicer default message.

##### assertIsInstance

```python
assertIsInstance(self, obj, cls, msg=None)
```

Same as self.assertTrue(isinstance(obj, cls)), with a nicer
        default message.

##### assertIsNone

```python
assertIsNone(self, obj, msg=None)
```

Same as self.assertTrue(obj is None), with a nicer default message.

##### assertIsNot

```python
assertIsNot(self, expr1, expr2, msg=None)
```

Just like self.assertTrue(a is not b), but with a nicer default message.

##### assertIsNotNone

```python
assertIsNotNone(self, obj, msg=None)
```

Included for symmetry with assertIsNone.

##### assertLess

```python
assertLess(self, a, b, msg=None)
```

Just like self.assertTrue(a < b), but with a nicer default message.

##### assertLessEqual

```python
assertLessEqual(self, a, b, msg=None)
```

Just like self.assertTrue(a <= b), but with a nicer default message.

##### assertListEqual

```python
assertListEqual(self, list1, list2, msg=None)
```

A list-specific equality assertion.

        Args:
            list1: The first list to compare.
            list2: The second list to compare.
            msg: Optional message to use on failure instead of a list of
                    differences.

###### Parameters

- **list1**: The first list to compare.
- **list2**: The second list to compare.
- **msg**: Optional message to use on failure instead of a list of
                    differences.

##### assertLogs

```python
assertLogs(self, logger=None, level=None)
```

Fail unless a log message of level *level* or higher is emitted
        on *logger_name* or its children.  If omitted, *level* defaults to
        INFO and *logger* defaults to the root logger.

        This method must be used as a context manager, and will yield
        a recording object with two attributes: `output` and `records`.
        At the end of the context manager, the `output` attribute will
        be a list of the matching formatted log messages and the
        `records` attribute will be a list of the corresponding LogRecord
        objects.

        Example::

            with self.assertLogs('foo', level='INFO') as cm:
                logging.getLogger('foo').info('first message')
                logging.getLogger('foo.bar').error('second message')
            self.assertEqual(cm.output, ['INFO:foo:first message',
                                         'ERROR:foo.bar:second message'])

##### assertMultiLineEqual

```python
assertMultiLineEqual(self, first, second, msg=None)
```

Assert that two multi-line strings are equal.

##### assertNoLogs

```python
assertNoLogs(self, logger=None, level=None)
```

Fail unless no log messages of level *level* or higher are emitted
        on *logger_name* or its children.

        This method must be used as a context manager.

##### assertNotAlmostEqual

```python
assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None)
```

Fail if the two objects are equal as determined by their
           difference rounded to the given number of decimal places
           (default 7) and comparing to zero, or by comparing that the
           difference between the two objects is less than the given delta.

           Note that decimal places (from zero) are usually not the same
           as significant digits (measured from the most significant digit).

           Objects that are equal automatically fail.

##### assertNotEqual

```python
assertNotEqual(self, first, second, msg=None)
```

Fail if the two objects are equal as determined by the '!='
           operator.

##### assertNotIn

```python
assertNotIn(self, member, container, msg=None)
```

Just like self.assertTrue(a not in b), but with a nicer default message.

##### assertNotIsInstance

```python
assertNotIsInstance(self, obj, cls, msg=None)
```

Included for symmetry with assertIsInstance.

##### assertNotRegex

```python
assertNotRegex(self, text, unexpected_regex, msg=None)
```

Fail the test if the text matches the regular expression.

##### assertRaises

```python
assertRaises(self, expected_exception, *args, **kwargs)
```

Fail unless an exception of class expected_exception is raised
           by the callable when invoked with specified positional and
           keyword arguments. If a different type of exception is
           raised, it will not be caught, and the test case will be
           deemed to have suffered an error, exactly as for an
           unexpected exception.

           If called with the callable and arguments omitted, will return a
           context object used like this::

                with self.assertRaises(SomeException):
                    do_something()

           An optional keyword argument 'msg' can be provided when assertRaises
           is used as a context object.

           The context manager keeps a reference to the exception as
           the 'exception' attribute. This allows you to inspect the
           exception after the assertion::

               with self.assertRaises(SomeException) as cm:
                   do_something()
               the_exception = cm.exception
               self.assertEqual(the_exception.error_code, 3)

##### assertRaisesRegex

```python
assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs)
```

Asserts that the message in a raised exception matches a regex.

        Args:
            expected_exception: Exception class expected to be raised.
            expected_regex: Regex (re.Pattern object or string) expected
                    to be found in error message.
            args: Function to be called and extra positional args.
            kwargs: Extra kwargs.
            msg: Optional message used in case of failure. Can only be used
                    when assertRaisesRegex is used as a context manager.

###### Parameters

- **expected_exception**: Exception class expected to be raised.
- **expected_regex**: Regex (re.Pattern object or string) expected
                    to be found in error message.
- **args**: Function to be called and extra positional args.
- **kwargs**: Extra kwargs.

##### assertRegex

```python
assertRegex(self, text, expected_regex, msg=None)
```

Fail the test unless the text matches the regular expression.

##### assertSequenceEqual

```python
assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None)
```

An equality assertion for ordered sequences (like lists and tuples).

        For the purposes of this function, a valid ordered sequence type is one
        which can be indexed, has a length, and has an equality operator.

        Args:
            seq1: The first sequence to compare.
            seq2: The second sequence to compare.
            seq_type: The expected datatype of the sequences, or None if no
                    datatype should be enforced.
            msg: Optional message to use on failure instead of a list of
                    differences.

###### Parameters

- **seq1**: The first sequence to compare.
- **seq2**: The second sequence to compare.
- **msg**: Optional message to use on failure instead of a list of
                    differences.
- **seq_type**: The expected datatype of the sequences, or None if no
                    datatype should be enforced.

##### assertSetEqual

```python
assertSetEqual(self, set1, set2, msg=None)
```

A set-specific equality assertion.

        Args:
            set1: The first set to compare.
            set2: The second set to compare.
            msg: Optional message to use on failure instead of a list of
                    differences.

        assertSetEqual uses ducktyping to support different types of sets, and
        is optimized for sets specifically (parameters must support a
        difference method).

###### Parameters

- **set1**: The first set to compare.
- **set2**: The second set to compare.
- **msg**: Optional message to use on failure instead of a list of
                    differences.

        assertSetEqual uses ducktyping to support different types of sets, and
        is optimized for sets specifically (parameters must support a
        difference method).

##### assertTrue

```python
assertTrue(self, expr, msg=None)
```

Check that the expression is true.

##### assertTupleEqual

```python
assertTupleEqual(self, tuple1, tuple2, msg=None)
```

A tuple-specific equality assertion.

        Args:
            tuple1: The first tuple to compare.
            tuple2: The second tuple to compare.
            msg: Optional message to use on failure instead of a list of
                    differences.

###### Parameters

- **tuple1**: The first tuple to compare.
- **tuple2**: The second tuple to compare.
- **msg**: Optional message to use on failure instead of a list of
                    differences.

##### assertWarns

```python
assertWarns(self, expected_warning, *args, **kwargs)
```

Fail unless a warning of class warnClass is triggered
           by the callable when invoked with specified positional and
           keyword arguments.  If a different type of warning is
           triggered, it will not be handled: depending on the other
           warning filtering rules in effect, it might be silenced, printed
           out, or raised as an exception.

           If called with the callable and arguments omitted, will return a
           context object used like this::

                with self.assertWarns(SomeWarning):
                    do_something()

           An optional keyword argument 'msg' can be provided when assertWarns
           is used as a context object.

           The context manager keeps a reference to the first matching
           warning as the 'warning' attribute; similarly, the 'filename'
           and 'lineno' attributes give you information about the line
           of Python code from which the warning was triggered.
           This allows you to inspect the warning after the assertion::

               with self.assertWarns(SomeWarning) as cm:
                   do_something()
               the_warning = cm.warning
               self.assertEqual(the_warning.some_attribute, 147)

##### assertWarnsRegex

```python
assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs)
```

Asserts that the message in a triggered warning matches a regexp.
        Basic functioning is similar to assertWarns() with the addition
        that only warnings whose messages also match the regular expression
        are considered successful matches.

        Args:
            expected_warning: Warning class expected to be triggered.
            expected_regex: Regex (re.Pattern object or string) expected
                    to be found in error message.
            args: Function to be called and extra positional args.
            kwargs: Extra kwargs.
            msg: Optional message used in case of failure. Can only be used
                    when assertWarnsRegex is used as a context manager.

###### Parameters

- **expected_warning**: Warning class expected to be triggered.
- **expected_regex**: Regex (re.Pattern object or string) expected
                    to be found in error message.
- **args**: Function to be called and extra positional args.
- **kwargs**: Extra kwargs.

##### countTestCases

```python
countTestCases(self)
```

##### debug

```python
debug(self)
```

Run the test without collecting errors in a TestResult

##### defaultTestResult

```python
defaultTestResult(self)
```

##### doCleanups

```python
doCleanups(self)
```

Execute all cleanup functions. Normally called for you after
        tearDown.

##### enterContext

```python
enterContext(self, cm)
```

Enters the supplied context manager.

        If successful, also adds its __exit__ method as a cleanup
        function and returns the result of the __enter__ method.

##### fail

```python
fail(self, msg=None)
```

Fail immediately, with the given message.

##### id

```python
id(self)
```

##### run

```python
run(self, result=None)
```

##### setUp

```python
setUp(self)
```

Set up test database.

##### shortDescription

```python
shortDescription(self)
```

Returns a one-line description of the test, or None if no
        description has been provided.

        The default implementation of this method returns the first line of
        the specified test method's docstring.

##### skipTest

```python
skipTest(self, reason)
```

Skip this test.

##### subTest

```python
subTest(self, msg=<object object at 0x7f1809361330>, **params)
```

Return a context manager that will return the enclosed block
        of code in a subtest identified by the optional message and
        keyword parameters.  A failure in the subtest marks the test
        case as failed but resumes execution at the end of the enclosed
        block, allowing further test code to be executed.

##### tearDown

```python
tearDown(self)
```

Clean up after tests.

##### test_get_relevant_memory

```python
test_get_relevant_memory(self)
```

Test retrieving relevant memories.

##### test_init_memory_db

```python
test_init_memory_db(self)
```

Test database initialization.

##### test_update_memory

```python
test_update_memory(self)
```

Test adding memory to database and deque.

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

### patch

```python
patch(target, new=sentinel.DEFAULT, spec=None, create=False, spec_set=None, autospec=None, new_callable=None, unsafe=False, **kwargs)
```

`patch` acts as a function decorator, class decorator or a context
    manager. Inside the body of the function or with statement, the `target`
    is patched with a `new` object. When the function/with statement exits
    the patch is undone.

    If `new` is omitted, then the target is replaced with an
    `AsyncMock if the patched object is an async function or a
    `MagicMock` otherwise. If `patch` is used as a decorator and `new` is
    omitted, the created mock is passed in as an extra argument to the
    decorated function. If `patch` is used as a context manager the created
    mock is returned by the context manager.

    `target` should be a string in the form `'package.module.ClassName'`. The
    `target` is imported and the specified object replaced with the `new`
    object, so the `target` must be importable from the environment you are
    calling `patch` from. The target is imported when the decorated function
    is executed, not at decoration time.

    The `spec` and `spec_set` keyword arguments are passed to the `MagicMock`
    if patch is creating one for you.

    In addition you can pass `spec=True` or `spec_set=True`, which causes
    patch to pass in the object being mocked as the spec/spec_set object.

    `new_callable` allows you to specify a different class, or callable object,
    that will be called to create the `new` object. By default `AsyncMock` is
    used for async functions and `MagicMock` for the rest.

    A more powerful form of `spec` is `autospec`. If you set `autospec=True`
    then the mock will be created with a spec from the object being replaced.
    All attributes of the mock will also have the spec of the corresponding
    attribute of the object being replaced. Methods and functions being
    mocked will have their arguments checked and will raise a `TypeError` if
    they are called with the wrong signature. For mocks replacing a class,
    their return value (the 'instance') will have the same spec as the class.

    Instead of `autospec=True` you can pass `autospec=some_object` to use an
    arbitrary object as the spec instead of the one being replaced.

    By default `patch` will fail to replace attributes that don't exist. If
    you pass in `create=True`, and the attribute doesn't exist, patch will
    create the attribute for you when the patched function is called, and
    delete it again afterwards. This is useful for writing tests against
    attributes that your production code creates at runtime. It is off by
    default because it can be dangerous. With it switched on you can write
    passing tests against APIs that don't actually exist!

    Patch can be used as a `TestCase` class decorator. It works by
    decorating each test method in the class. This reduces the boilerplate
    code when your test methods share a common patchings set. `patch` finds
    tests by looking for method names that start with `patch.TEST_PREFIX`.
    By default this is `test`, which matches the way `unittest` finds tests.
    You can specify an alternative prefix by setting `patch.TEST_PREFIX`.

    Patch can be used as a context manager, with the with statement. Here the
    patching applies to the indented block after the with statement. If you
    use "as" then the patched object will be bound to the name after the
    "as"; very useful if `patch` is creating a mock object for you.

    Patch will raise a `RuntimeError` if passed some common misspellings of
    the arguments autospec and spec_set. Pass the argument `unsafe` with the
    value True to disable that check.

    `patch` takes arbitrary keyword arguments. These will be passed to
    `AsyncMock` if the patched object is asynchronous, to `MagicMock`
    otherwise or to `new_callable` if specified.

    `patch.dict(...)`, `patch.multiple(...)` and `patch.object(...)` are
    available for alternate use-cases.

### update_memory

```python
update_memory(conn: sqlite3.Connection, query: str, result: Dict[str, Any], short_term_memory: Deque)
```

