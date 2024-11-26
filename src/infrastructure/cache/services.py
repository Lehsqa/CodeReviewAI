import json
from typing import Any, Generic, get_args

from redis.asyncio import Redis
from redis.asyncio.client import Pipeline

from src.config import settings

from ..application import InternalEntity, NotFoundError
from .entities import CacheEntry, _CacheEntryInstance

__all__ = ("CacheRepository",)


# TODO: Add a single transaction context manager


class CacheRepository(Generic[_CacheEntryInstance]):
    """This class is a gateway to the Redis cache.
    Usage example:

        >>> from src.infrastructure.cache import CacheRepository
        >>> from src.domain.users import UserFlat, UsersRepository

        >>> entry: CacheEntry[InternalModel] = (
                await CacheRepository[InternalModel]().set(
                    namespace="users", key=1, instance=user
                )
            )

        >>> entry: CacheEntry[InternalModel] = (
                async with CacheRepository[InternalModel]() as cache:
                    await cache.get(
                        namespace="users", key=1
                    )
                )
    """

    def __init__(self):
        self.redis_client: Redis | None = None
        self.transaction: Pipeline | None = None

    async def __aenter__(self) -> "CacheRepository[_CacheEntryInstance]":
        """Connect to the Redis cache."""

        self.redis_client = Redis(
            host=settings.cache.host,
            port=settings.cache.port,
            db=settings.cache.db,
        )

        self.transaction = self.redis_client.pipeline(transaction=True)
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        assert self.redis_client is not None
        assert self.transaction is not None

        if exc_type is None:
            await self.transaction.execute()

        await self.redis_client.close()

        self.redis_client = None
        self.transaction = None

    def _build_key(self, namespace: str, key: Any) -> str:
        """Returns a key with the additional namespace for this cache."""

        return f"{namespace}:{str(key)}"

    async def get(
        self, namespace: str, key: Any
    ) -> CacheEntry[_CacheEntryInstance]:
        """Get the item from the cache by the key."""

        assert self.redis_client is not None
        assert self.transaction is not None

        if results := (
            await self.transaction.get(
                self._build_key(namespace=namespace, key=key)
            ).execute()  # type: ignore
        ):
            try:
                raw: dict[str, Any] = json.loads(results[0])
            except (json.JSONDecodeError, TypeError):
                raise NotFoundError(
                    message=f"Cache entry not found. Key: {key}"
                )

            generic_class_ = get_args(self.__orig_class__)[0]  # type: ignore
            return CacheEntry[_CacheEntryInstance](
                instance=generic_class_(**raw["instance"])
            )

        raise NotFoundError(message=f"Cache entry not found. Key: {key}")

    async def set(
        self,
        namespace: str,
        key: Any,
        instance: InternalEntity,
        ttl: int | None = None,
    ) -> CacheEntry[_CacheEntryInstance]:
        """Saves the CacheEntry instance to the cache."""

        assert self.redis_client is not None
        assert self.transaction is not None

        entry: CacheEntry[_CacheEntryInstance] = CacheEntry(instance=instance)

        await self.transaction.set(
            name=self._build_key(namespace=namespace, key=key),
            value=entry.model_dump_json(),
            ex=ttl,
        ).execute()  # type: ignore

        return entry

    async def delete(self, namespace: str, key: Any) -> None:
        """Delete the item from the cache by the key."""

        assert self.redis_client is not None
        assert self.transaction is not None

        await self.transaction.delete(
            self._build_key(namespace=namespace, key=key),
        ).execute()  # type: ignore
