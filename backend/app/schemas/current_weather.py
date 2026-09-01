from datetime import datetime

from pydantic import BaseModel


class CurrentWeatherResponse(BaseModel):
    ts: datetime

    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    dew_point: float

    unit_temperature: str
    unit_humidity: str
    unit_pressure: str
    unit_wind_speed: str
    unit_dew_point: str