from fastapi import APIRouter

from backend.app.schemas.city import (
    CityRequest,
    CityResponse,
)
from backend.app.services.city import (
    get_city_prediction,
)


router = APIRouter(
    prefix="/api",
    tags=["City"],
)


@router.post(
    "/city",
    response_model=CityResponse,
)
def city_prediction(
    request: CityRequest,
) -> CityResponse:
    return get_city_prediction(
        latitude=request.latitude,
        longitude=request.longitude,
    )