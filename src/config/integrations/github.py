from pydantic import BaseModel


class GitHubSettings(BaseModel):
    api_key: str = "invalid"
    api_url: str = "invalid"
    accept: str = "invalid"


class APISettings(BaseModel):
    github: GitHubSettings = GitHubSettings()


class Settings(BaseModel):
    api: APISettings = APISettings()
