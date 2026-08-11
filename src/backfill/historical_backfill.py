import pandas as pd

from src.feature_pipeline.constants import OPENMETEO_WEATHER_HISTORICAL_URL
from src.feature_pipeline.data_collector import collect_features
from src.feature_pipeline.hopsworks_client import raw_hourly_fs
from src.feature_pipeline.schemas import FeatureDict, DateRanges


def run_historical_backfill(historical_backfill_dates: DateRanges | None = None) -> None:
    """
        Run the historical backfill pipeline

        :param historical_backfill_dates: List of date ranges
        :return: None
    """

    if historical_backfill_dates is None:
        historical_backfill_dates: DateRanges = [("2025-11-08", "2026-02-07"), ("2026-02-08", "2026-05-07"), ("2026-05-08", "2026-08-08")]

    historical_backfill_features: list[FeatureDict] = []

    # For each date range
    for date_range in historical_backfill_dates:
        features = collect_features(OPENMETEO_WEATHER_HISTORICAL_URL, "BACKFILL", date_range)

        if features is not None:
            historical_backfill_features.extend(features)

    df = pd.DataFrame(historical_backfill_features)

    # Insert into the feature store for raw data
    raw_hourly_fs.insert(df)