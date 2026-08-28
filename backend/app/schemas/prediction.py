from datetime import datetime

from pydantic import BaseModel


class AQIPredictionResponse(BaseModel):
    aqi_pred_day_1: float
    aqi_pred_day_2: float
    aqi_pred_day_3: float
    aqi_pred_day_4: float
    ts: datetime