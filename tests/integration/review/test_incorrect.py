import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
async def test_invalid_github_url():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/review", json={
            "assignment_description": "Test",
            "github_repo_url": "invalid_url",
            "candidate_level": "Senior"
        })
    assert response.status_code == 400
