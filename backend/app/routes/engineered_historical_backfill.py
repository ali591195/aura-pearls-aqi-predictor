from fastapi import APIRouter, HTTPException

from backend.app.schemas.backfill import HistoricalBackfillResponse
from backend.app.services.engineered_historical_backfill import backfill_engineered_historical_data
from backend.app.utils.routes import raise_internal_server_error

router = APIRouter(
    prefix="/api/backfill",
    tags=["Backfill"],
)


@router.post(
    "/engineered",
    response_model=HistoricalBackfillResponse,
)
def run_engineered_historical_backfill() -> (
    HistoricalBackfillResponse | None
):
    try:
        return backfill_engineered_historical_data()

    except RuntimeError as error:
        raise_internal_server_error(error)