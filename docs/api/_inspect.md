# _inspect

Subset of inspect module from upstream python

We use this instead of upstream because upstream inspect is slow to import, and
significantly contributes to numpy import times. Importing this copy has almost
no overhead.

