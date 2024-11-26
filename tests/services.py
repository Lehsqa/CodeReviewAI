import json
from typing import Any

from src.config import settings


def mock_read(path: str) -> Any:
    """Read the mocked data from the file in mock directory.

    [Usage]
    >>> payload: Any = read_mocked("google.geocoding.response_200.json")

    This will read the /tests/mocks/google/geocoding/response_200.json file.
    """

    with open(settings.root_dir / f"tests/mock/{path}") as file:
        return json.load(file)
