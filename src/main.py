from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from loguru import logger

from src import presentation
from src.config import settings
from src.infrastructure.application import BaseError, base_error_handler
from src.infrastructure.application import create as application_factory
from src.infrastructure.application import (
    fastapi_http_exception_handler,
    middlewares,
    not_implemented_error_handler,
    unhandled_error_handler,
    unprocessable_entity_error_handler,
)

# Adjust the logging
# -------------------------------
logger.add(
    "".join(
        [
            str(settings.root_dir),
            "/logs/",
            settings.logging.file.lower(),
            ".log",
        ]
    ),
    format=settings.logging.format,
    rotation=settings.logging.rotation,
    compression=settings.logging.compression,
    level="INFO",
)


rest_routers: list[APIRouter] = [
    presentation.review.rest.router,
]

# Adjust the application
# -------------------------------
app: FastAPI = application_factory(
    title=settings.public_api.name,
    version=settings.public_api.version,
    debug=settings.debug,
    rest_routers=rest_routers,
    middlewares=(
        (middlewares.cors.CORSMiddleware, middlewares.cors.OPTIONS),
        (middlewares.sessions.SessionMiddleware, middlewares.sessions.OPTIONS),
    ),
    exception_handlers={
        RequestValidationError: unprocessable_entity_error_handler,
        HTTPException: fastapi_http_exception_handler,
        NotImplementedError: not_implemented_error_handler,
        BaseError: base_error_handler,
        Exception: unhandled_error_handler,
    },
)
