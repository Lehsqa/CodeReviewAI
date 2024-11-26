from pydantic import BaseModel


class Settings(BaseModel):
    """Configure the logging engine."""

    # The time field can be formatted using more human-friendly tokens.
    # These constitute a subset of the one used by the Pendulum library
    # https://pendulum.eustace.io/docs/#tokens
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <5} | {message}"

    # The .log filename
    file: str = "code-review-ai"

    # The .log file Rotation
    rotation: str = "10MB"

    # The type of compression
    compression: str = "zip"
