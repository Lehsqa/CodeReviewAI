from typing import List

from src.infrastructure.application import PublicEntity

__all__ = ("Result",)


class Result(PublicEntity):
    code_contents: str
    file_contents: List[str]
