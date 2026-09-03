from fastapi import APIRouter, HTTPException

from backend.app.schemas.current_weather import (
    CurrentWeatherResponse,
)
from backend.app.services.current_weather import (
    fetch_current_weather,
)
from backend.app.utils.routes import raise_bad_gateway_error

router = APIRouter(
    prefix="/api",
    tags=["Current Weather"],
)


@router.get(
    "/current-weather",
    response_model=CurrentWeatherResponse,
)
def get_current_weather() -> CurrentWeatherResponse | None:
    try:
        return fetch_current_weather()

    except RuntimeError as error:
        raise_bad_gateway_error(error)