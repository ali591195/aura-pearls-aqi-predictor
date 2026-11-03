from datetime import datetime, timedelta, timezone

from pandas import DataFrame

from backend.app.utils.backfill import get_latest_raw_timestamp
from src.common.hopsworks_client import engineered_daily_fs


def get_features() -> DataFrame:
    """
    Get the latest available engineered features.

    :return: Latest engineered feature row as a DataFrame.
    """

    today = datetime.now(timezone.utc).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    yesterday = today - timedelta(days=1)

    df = engineered_daily_fs.read(
        start_time=yesterday,
        end_time=today
    )

    if df.empty:
        # Data is stale: fall back to the latest available row, however old.
        latest_timestamp = get_latest_raw_timestamp(engineered_daily_fs)

        if latest_timestamp is None:
            raise RuntimeError("No engineered features are available.")

        latest_day = latest_timestamp.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        df = engineered_daily_fs.read(
            start_time=latest_day,
            end_time=latest_day + timedelta(days=1)
        )

        return df.sort_values("ts").tail(1)

    return df