from datetime import date, datetime, timedelta

import pandas as pd
from hsfs.feature_group import ExternalFeatureGroup, SpineGroup, FeatureGroup


def get_latest_raw_timestamp(fs: FeatureGroup | ExternalFeatureGroup | SpineGroup) -> datetime | None:
    """
    Get the latest timestamp currently stored in the raw hourly
    feature group.
    """

    latest_data = (
        fs
        .select(["ts"])
        .read(dataframe_type="pandas")
    )

    if latest_data.empty:
        return None

    latest_timestamp = pd.to_datetime(
        latest_data["ts"],
        utc=True,
    ).max()

    if pd.isna(latest_timestamp):
        return None

    return latest_timestamp.to_pydatetime()

def get_backfill_start_date(fs: FeatureGroup | ExternalFeatureGroup | SpineGroup) -> date:
    latest_timestamp = get_latest_raw_timestamp(fs)

    if latest_timestamp is None:
        raise RuntimeError(
            "No existing raw hourly data was found."
        )

    start_date = latest_timestamp.date() - timedelta(days=1)

    return start_date

def validate_backfill_date_range(
    start_date: date,
    end_date: date,
) -> None:
    if start_date > end_date:
        raise RuntimeError(
            "Calculated backfill start date is after the end date."
        )