from typing import Any

from fastapi import HTTPException

from src.domain.review.entities import ReviewUncommited
from src.infrastructure.application import NotFoundError, BadRequestError
from src.infrastructure.cache import CacheRepository
from src.integrations.github.contracts import Result as GithubResult
from src.integrations.openai.contracts import Result as OpenAIResult
from src.integrations.github.services import fetch_repository_contents
from src.integrations.openai import analyze_code

from urllib.parse import urlparse

__all__ = ("generate",)


def validate_github_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc == "github.com" and len(parsed.path.strip("/").split("/")) >= 2


async def generate(request: dict[str, Any]) -> ReviewUncommited:
    async with CacheRepository[ReviewUncommited]() as cache:
        try:
            if result_cache := await cache.get(
                namespace="review", key=request
            ):
                return result_cache.instance
        except NotFoundError:
            pass

    if not validate_github_url(str(request["github_repo_url"])):
        raise BadRequestError(message="Invalid GitHub repository URL.")

    # Fetch repository contents
    github: GithubResult = await fetch_repository_contents(str(request["github_repo_url"]))

    # Analyze code using OpenAI API
    review: OpenAIResult = await analyze_code(
        assignment_description=request["assignment_description"],
        code_contents=github.code_contents,
        candidate_level=request["candidate_level"]
    )

    result: ReviewUncommited = ReviewUncommited(
        found_files=github.file_contents,
        **review.model_dump()
    )

    # Save the activation key to the cache
    async with CacheRepository[ReviewUncommited]() as cache:
        await cache.set(
            namespace="review", key=request, instance=result
        )

    return result
