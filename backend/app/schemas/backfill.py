from datetime import date

from pydantic import BaseModel


class HistoricalBackfillResponse(BaseModel):
    message: str
    start_date: date
    end_date: date