from datetime import datetime
from typing import Generic, TypeVar

from pydantic import Field

from ..application import InternalEntity

__all__ = ("CacheEntry", "_CacheEntryInstance")

_CacheEntryInstance = TypeVar("_CacheEntryInstance", bound=InternalEntity)


class CacheEntry(InternalEntity, Generic[_CacheEntryInstance]):
    """This data model represents a cache entry.
    The instance could be anything that is serializable with pydantic.
    """

    instance: _CacheEntryInstance
    created_at: datetime = Field(default_factory=datetime.utcnow)
