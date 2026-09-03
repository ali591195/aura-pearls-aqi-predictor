from datetime import datetime, timedelta, timezone

from backend.app.schemas.backfill import HistoricalBackfillResponse
from backend.app.utils.backfill import get_backfill_start_date, validate_backfill_date_range
from src.backfill.historical_backfill import generate_backfill_date_ranges, run_historical_backfill
from src.common.hopsworks_client import raw_hourly_fs
from src.common.schemas import DateRanges


def backfill_raw_historical_data() -> HistoricalBackfillResponse:
    """
    Find the latest raw reading, start backfilling from the day before
    that reading, and continue through today.
    """

    now = datetime.now(timezone.utc)

    start_date = get_backfill_start_date(raw_hourly_fs)
    end_date = now.date()

    validate_backfill_date_range(start_date, end_date)

    historical_backfill_dates: DateRanges = (
        generate_backfill_date_ranges(
            start_date.isoformat(),
            end_date.isoformat(),
        )
    )

    run_historical_backfill(
        historical_backfill_dates
    )

    return HistoricalBackfillResponse(
        message="Raw historical backfill completed successfully.",
        start_date=start_date,
        end_date=end_date,
    )