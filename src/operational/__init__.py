"""
This layer represents all sorts of operations that represent business logic.
According to the Layered Architecture, it could be called
the Application Layer as well.

Since the main entrypoint is a Presentation Layer, this layer
delegates all the work accross the Domain and the Infrastructure layers.
"""

from . import review  # noqa: F401
