import logging
from typing import AsyncGenerator
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from httpx import AsyncClient
from loguru import logger

from src import presentation
from src.config import settings
from src.infrastructure.application import BaseError, base_error_handler
from src.infrastructure.application import create as application_factory
from src.infrastructure.application import (
    fastapi_http_exception_handler,
    not_implemented_error_handler,
    unhandled_error_handler,
    unprocessable_entity_error_handler,
)
from src.infrastructure.cache import CacheRepository
from src.infrastructure.cache.tests import TestCacheRepository


def pytest_configure():
    # Disable logs
    logging.disable(
        logging.CRITICAL
    )  # This disables all logging below CRITICAL

    logger.disable("src.infrastructure")
    logger.disable("src.presentation")
    logger.disable("src.domain")
    logger.disable("src.operational")


# =====================================================================
# Cache specific fixtures and mocks
# =====================================================================
@pytest.fixture(autouse=True)
def patch_cache_service(mocker) -> MagicMock:
    """This fixture patches the cache service to use the in-memory
    cache repository.
    """

    return mocker.patch.object(
        CacheRepository, "__new__", return_value=TestCacheRepository()
    )


@pytest.fixture(autouse=True)
def auto_clean_cache_storage(mocker):
    """This fixture automatically cleans the cache storage
    for each test separately.
    """

    yield
    TestCacheRepository._store = {}


# =====================================================================
# Application specific fixtures
# =====================================================================
@pytest.fixture
def app() -> FastAPI:
    return application_factory(
        debug=settings.debug,
        rest_routers=(
            presentation.review.rest.router,
        ),
        exception_handlers={
            RequestValidationError: unprocessable_entity_error_handler,
            HTTPException: fastapi_http_exception_handler,
            NotImplementedError: not_implemented_error_handler,
            BaseError: base_error_handler,
            Exception: unhandled_error_handler,
        },
    )


@pytest.fixture
async def anonymous(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Returns the client without the authorized user."""

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
