import functools
import json
from typing import Any

import pytest

from src.config import settings


@pytest.fixture
def mock_read():
    """This fixture reads the mocked data from the file.

    [Usage]
    >>> payload: Any = read_mocked("google.geocoding.response_200.json")

    This will read the /tests/mocks/google/geocoding/response_200.json file.
    """

    @functools.wraps(mock_read)
    def inner(path: str) -> Any:
        with open(settings.root_dir / f"tests/mock/{path}") as file:
            return json.load(file)

    return inner
