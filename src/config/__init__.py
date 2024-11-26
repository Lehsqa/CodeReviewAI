"""This module defines the application settings."""


from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from . import cache as _cache
from . import core
from . import cors as _cors
from . import integrations as _integrations
from . import logging as _logging
from . import public_api as _public_api

__all__ = ("settings",)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )

    # Infrastructure settings
    cache: _cache.Settings = _cache.Settings()

    # Application settings
    root_dir: Path
    src_dir: Path

    debug: bool = True
    public_api: _public_api.Settings = _public_api.Settings()
    logging: _logging.Settings = _logging.Settings()
    cors: _cors.Settings = _cors.Settings()

    # 👽 Integrations settings
    integrations: _integrations.Settings = _integrations.Settings()


# ======================================
# Load settings
# ======================================
settings = Settings(
    # NOTE: We would like to hard-code the root and applications directories
    #       to avoid overriding via environment variables
    root_dir=core.ROOT_PATH,
    src_dir=core.ROOT_PATH / "src",
)
