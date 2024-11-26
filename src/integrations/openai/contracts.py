from src.infrastructure.application import PublicEntity

__all__ = ("Result",)


class Result(PublicEntity):
    downsides_comments: str
    rating: str
    conclusion: str
