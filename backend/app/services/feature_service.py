from datetime import datetime, timedelta, timezone

from pandas import DataFrame

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
        # Get the latest available row.
        start_date = yesterday - timedelta(days=29)

        df = engineered_daily_fs.read(
            start_time=start_date,
            end_time=today
        )

        return df.sort_values("ts").tail(1)

    return df