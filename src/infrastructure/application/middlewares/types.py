from typing import Protocol

from starlette.types import Receive, Scope, Send

__all__ = ("Middleware",)


class Middleware(Protocol):
    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        ...
