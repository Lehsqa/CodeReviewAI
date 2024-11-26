from datetime import datetime

__all__ = ("TimeStampMixin",)


class TimeStampMixin:
    """This Mixin extends internal or public entity with timestamps."""

    created_at: datetime
    updated_at: datetime
