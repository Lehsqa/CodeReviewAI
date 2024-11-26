from typing import List

from pydantic import field_validator, AnyHttpUrl

from src.infrastructure.application import PublicEntity

__all__ = ("ReviewRequest", "ReviewResponse")


class ReviewRequest(PublicEntity):
    assignment_description: str
    github_repo_url: AnyHttpUrl
    candidate_level: str

    @field_validator("candidate_level", mode="before")
    def candidate_level_is_allowed(cls, value: str) -> str:
        """Check if the role is allowed."""

        if value not in ["Junior", "Middle", "Senior"]:
            raise ValueError(f"The role {value} is not allowed.")

        return value


class ReviewResponse(PublicEntity):
    found_files: List[str]
    downsides_comments: str
    rating: str
    conclusion: str
