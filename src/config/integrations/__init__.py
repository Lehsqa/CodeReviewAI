from pydantic import BaseModel

from . import github as _github
from . import openai as _openai

__all__ = ("Settings",)


class Settings(BaseModel):
    github: _github.Settings = _github.Settings()
    openai: _openai.Settings = _openai.Settings()
