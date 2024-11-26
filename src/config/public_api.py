"""
This module includes all the settings related
to the application representation as a public API service.
"""

from pydantic import BaseModel


class APIUrlsSettings(BaseModel):
    """API public urls settings."""

    docs: str = "/docs"
    redoc: str = "/redoc"


class Settings(BaseModel):
    """Configure public API service settings."""

    domain: str = "http://backend.com"
    name: str = "Code Review AI"
    version: str = "0.1.0"
    urls: APIUrlsSettings = APIUrlsSettings()
