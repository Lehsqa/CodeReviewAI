import json
from typing import Any, Generic, get_args

from src.infrastructure.application import InternalEntity, NotFoundError
from src.infrastructure.cache import (
    CacheEntry,
    CacheRepository,
    _CacheEntryInstance,
)

__all__ = ("TestCacheRepository",)


class TestCacheRepository(CacheRepository, Generic[_CacheEntryInstance]):
    _store: dict[str, str] = {}  # In-memory store to simulate Redis

    def __init__(self):
        pass

    async def __aenter__(self) -> "TestCacheRepository[_CacheEntryInstance]":
        # Override to not connect to actual Redis
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        # Override to not close actual Redis connection
        pass

    async def get(
        self, namespace: str, key: Any
    ) -> CacheEntry[_CacheEntryInstance]:
        # Override to get from the in-memory store
        full_key = self._build_key(namespace, key)
        if full_key in self._store:
            raw = json.loads(self._store[full_key])
            generic_class_ = get_args(self.__orig_class__)[0]  # type: ignore
            return CacheEntry[_CacheEntryInstance](
                instance=generic_class_(**raw["instance"])
            )
        else:
            raise NotFoundError(message=f"Cache entry not found. Key: {key}")

    async def set(
        self,
        namespace: str,
        key: Any,
        instance: InternalEntity,
        ttl: int | None = None,
    ) -> CacheEntry[_CacheEntryInstance]:
        # Override to set in the in-memory store
        full_key = self._build_key(namespace, key)
        entry = CacheEntry[_CacheEntryInstance](instance=instance)
        self._store[full_key] = entry.model_dump_json()
        return entry

    async def delete(self, namespace: str, key: Any) -> None:
        # Override to delete from the in-memory store
        full_key = self._build_key(namespace, key)
        self._store.pop(full_key, None)
