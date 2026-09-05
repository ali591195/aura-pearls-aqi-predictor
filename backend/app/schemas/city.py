from pydantic import BaseModel, Field

from backend.app.schemas.current_air_quality import (
    CurrentAirQualityResponse,
)
from backend.app.schemas.current_weather import (
    CurrentWeatherResponse,
)
from backend.app.schemas.prediction import (
    AQIPredictionResponse,
)


class CityRequest(BaseModel):
    latitude: float = Field(
        ge=-90,
        le=90,
    )
    longitude: float = Field(
        ge=-180,
        le=180,
    )


class CityResponse(BaseModel):
    prediction: AQIPredictionResponse
    current_air_quality: CurrentAirQualityResponse
    current_weather: CurrentWeatherResponse