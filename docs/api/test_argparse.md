# test_argparse

Tests for the private NumPy argument parsing functionality.
They mainly exists to ensure good test coverage without having to try the
weirder cases on actual numpy functions but test them in one place.

The test function is defined in C to be equivalent to (errors may not always
match exactly, and could be adjusted):

    def func(arg1, /, arg2, *, arg3):
        i = integer(arg1)  # reproducing the 'i' parsing in Python.
        return None

