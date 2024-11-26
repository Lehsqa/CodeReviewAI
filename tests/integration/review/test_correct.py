import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
async def test_review_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/review", json={
            "assignment_description": "Create a REST API",
            "github_repo_url": "https://github.com/valid/repo",
            "candidate_level": "Junior"
        })
    assert response.status_code == 200
    data = response.json()
    assert "found_files" in data
    assert "downsides_comments" in data
    assert "rating" in data
    assert "conclusion" in data
