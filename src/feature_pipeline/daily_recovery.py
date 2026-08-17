from datetime import datetime, UTC, timedelta

from src.common.constants import OPENMETEO_WEATHER_URL
from src.feature_pipeline.data_collector import collect_and_insert_features


def run_daily_recovery() -> None:
    """
        Run the daily recovery pipeline

        :return: None
    """

    yesterday = (datetime.now(UTC) - timedelta(days=1)).strftime("%Y-%m-%d")
    date_range = (yesterday, yesterday)

    collect_and_insert_features(OPENMETEO_WEATHER_URL, "BACKFILL", date_range)