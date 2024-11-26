from pydantic import BaseModel


class Settings(BaseModel):
    host: str = "cache"
    port: int = 6379
    db: int = 0
    ttl: int = 86400  # 24 hours
