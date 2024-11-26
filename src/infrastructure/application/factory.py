from typing import Iterable, Type

from fastapi import APIRouter, FastAPI

from .middlewares.types import Middleware

__all__ = ("create",)


def create(
    *_,
    rest_routers: Iterable[APIRouter],
    middlewares: Iterable[tuple[Type[Middleware], dict]] | None = None,
    **kwargs,
) -> FastAPI:
    """The application factory using FastAPI framework."""

    # Initialize the base FastAPI application
    app = FastAPI(**kwargs)

    # Include REST API routers
    for router in rest_routers:
        app.include_router(router)

    # Define middlewares using FastAPI hook
    if middlewares is not None:
        for middleware_class, options in middlewares:
            app.add_middleware(middleware_class, **options)

    # TODO: Add lifespan events:
    #       🔗 https://fastapi.tiangolo.com/advanced/events/#lifespan

    return app
