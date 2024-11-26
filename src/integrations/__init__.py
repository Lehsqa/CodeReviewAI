"""
This namespace includes all the integrations with external services.

⚠️ This folder should be encapsulated into the `infrastructure`, but since
the integration with external services is a very important part of the
application, it is placed at the root of the sources.
"""

from . import openai  # noqa: F401
from . import github  # noqa: F401
