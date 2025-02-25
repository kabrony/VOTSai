# exceptions

Exceptions and Warnings (:mod:`numpy.exceptions`)
=================================================

General exceptions used by NumPy.  Note that some exceptions may be module
specific, such as linear algebra errors.

.. versionadded:: NumPy 1.25

    The exceptions module is new in NumPy 1.25.  Older exceptions remain
    available through the main NumPy namespace for compatibility.

.. currentmodule:: numpy.exceptions

Warnings
--------
.. autosummary::
   :toctree: generated/

   ComplexWarning             Given when converting complex to real.
   VisibleDeprecationWarning  Same as a DeprecationWarning, but more visible.
   RankWarning                Issued when the design matrix is rank deficient.

Exceptions
----------
.. autosummary::
   :toctree: generated/

    AxisError          Given when an axis was invalid.
    DTypePromotionError   Given when no common dtype could be found.
    TooHardError       Error specific to `numpy.shares_memory`.

