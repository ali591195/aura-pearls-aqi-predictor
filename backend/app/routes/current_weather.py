from fastapi import APIRouter, HTTPException

from backend.app.schemas.current_weather import (
    CurrentWeatherResponse,
)
from backend.app.services.current_weather import (
    fetch_current_weather,
)

router = APIRouter(
    prefix="/api",
    tags=["Current Weather"],
)


@router.get(
    "/current-weather",
    response_model=CurrentWeatherResponse,
)
def get_current_weather() -> CurrentWeatherResponse:
    try:
        return fetch_current_weather()

    except RuntimeError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error