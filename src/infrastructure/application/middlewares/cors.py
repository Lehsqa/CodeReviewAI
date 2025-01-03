from fastapi.middleware.cors import CORSMiddleware as _CORSMiddleware

from src.config import settings


class CORSMiddleware(_CORSMiddleware):
    pass


OPTIONS: dict = {
    "allow_origins": settings.cors.allow_origins,
    "allow_credentials": settings.cors.allow_credentials,
    "allow_methods": settings.cors.allow_methods,
    "allow_headers": settings.cors.allow_headers,
    "expose_headers": settings.cors.expose_headers,
    "max_age": settings.cors.max_age,
}
