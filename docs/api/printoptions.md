# printoptions

Stores and defines the low-level format_options context variable.

This is defined in its own file outside of the arrayprint module
so we can import it from C while initializing the multiarray
C module during import without introducing circular dependencies.

