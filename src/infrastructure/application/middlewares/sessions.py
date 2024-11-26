from starlette.middleware.sessions import (
    SessionMiddleware as _SessionMiddleware,
)

from src.config import settings


class SessionMiddleware(_SessionMiddleware):
    pass


OPTIONS: dict = {"secret_key": "secret-key"}
