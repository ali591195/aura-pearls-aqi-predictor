from fastapi import APIRouter, HTTPException

from backend.app.schemas.current_air_quality import (
    CurrentAirQualityResponse,
)
from backend.app.services.current_air_quality import (
    fetch_current_air_quality,
)

router = APIRouter(
    prefix="/api",
    tags=["Current Air Quality"]
)


@router.get(
    "/current-air-quality",
    response_model=CurrentAirQualityResponse,
)
def get_current_air_quality() -> CurrentAirQualityResponse:
    try:
        return fetch_current_air_quality()

    except RuntimeError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error