from typing import List

from src.infrastructure.application import InternalEntity

__all__ = (
    "ReviewUncommited",
)


class ReviewUncommited(InternalEntity):
    found_files: List[str]
    downsides_comments: str
    rating: str
    conclusion: str
