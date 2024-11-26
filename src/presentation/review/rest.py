from fastapi import APIRouter, Body, Request, status

from src.infrastructure.application import Response

from .contracts import (
    ReviewRequest,
    ReviewResponse,
)
from src.operational.review import generate

router = APIRouter(prefix="", tags=["Review"])


# ************************************************
# ********** Review **********
# ************************************************
@router.post(
    "/review",
    response_model=Response[ReviewResponse],
    status_code=status.HTTP_201_CREATED,
)
async def review_code(
    _: Request, schema: ReviewRequest = Body(...)
) -> Response[ReviewResponse]:

    return Response[ReviewResponse](result=await generate(schema.dict()))
