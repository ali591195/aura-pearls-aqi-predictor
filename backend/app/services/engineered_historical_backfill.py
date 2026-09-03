from datetime import datetime, timedelta, timezone

from backend.app.schemas.backfill import HistoricalBackfillResponse
from backend.app.utils.backfill import get_backfill_start_date, validate_backfill_date_range
from src.backfill.engineered_features_backfill import run_engineered_features_backfill
from src.common.hopsworks_client import engineered_daily_fs


def backfill_engineered_historical_data() -> (
    HistoricalBackfillResponse
):
    """
    Find the latest raw reading, start engineered-data backfill
    from the day before that reading, and continue through yesterday.
    """

    now = datetime.now(timezone.utc)

    start_date = get_backfill_start_date(engineered_daily_fs)

    # end_date = (
    #     datetime.now(timezone.utc).date()
    #     - timedelta(days=1)
    # )
    end_date = now.date()

    validate_backfill_date_range(start_date, end_date)

    start_datetime = datetime.combine(
        start_date,
        datetime.min.time(),
        tzinfo=timezone.utc,
    )

    end_datetime = datetime.combine(
        end_date,
        datetime.max.time(),
        tzinfo=timezone.utc,
    )

    run_engineered_features_backfill(
        backfill_start_date=start_datetime,
        backfill_end_date=end_datetime,
    )

    return HistoricalBackfillResponse(
        message=(
            "Engineered historical backfill "
            "completed successfully."
        ),
        start_date=start_date,
        end_date=end_date,
    )