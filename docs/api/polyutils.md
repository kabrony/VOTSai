# polyutils

Utility classes and functions for the polynomial modules.

This module provides: error and warning objects; a polynomial base class;
and some routines used in both the `polynomial` and `chebyshev` modules.

Functions
---------

.. autosummary::
   :toctree: generated/

   as_series    convert list of array_likes into 1-D arrays of common type.
   trimseq      remove trailing zeros.
   trimcoef     remove small trailing coefficients.
   getdomain    return the domain appropriate for a given set of abscissae.
   mapdomain    maps points between domains.
   mapparms     parameters of the linear map between domains.

