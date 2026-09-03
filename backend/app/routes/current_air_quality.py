from fastapi import APIRouter, HTTPException

from backend.app.schemas.current_air_quality import (
    CurrentAirQualityResponse,
)
from backend.app.services.current_air_quality import (
    fetch_current_air_quality,
)
from backend.app.utils.routes import raise_bad_gateway_error

router = APIRouter(
    prefix="/api",
    tags=["Current Air Quality"]
)


@router.get(
    "/current-air-quality",
    response_model=CurrentAirQualityResponse,
)
def get_current_air_quality() -> CurrentAirQualityResponse | None:
    try:
        return fetch_current_air_quality()

    except RuntimeError as error:
        raise_bad_gateway_error(error)