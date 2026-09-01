from datetime import datetime

from pydantic import BaseModel


class CurrentAirQualityResponse(BaseModel):
    ts: datetime

    us_aqi: float
    today_us_aqi_mean: float

    pm10: float
    pm2_5: float
    carbon_monoxide: float
    nitrogen_dioxide: float
    sulphur_dioxide: float
    ozone: float

    unit_pm10: str
    unit_pm2_5: str
    unit_carbon_monoxide: str
    unit_nitrogen_dioxide: str
    unit_sulphur_dioxide: str
    unit_ozone: str