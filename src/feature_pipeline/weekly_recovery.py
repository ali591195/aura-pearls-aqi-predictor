from datetime import datetime, UTC, timedelta

from src.feature_pipeline.constants import OPENMETEO_WEATHER_URL
from src.feature_pipeline.data_collector import collect_and_insert_features


def run_weekly_recovery() -> None:
    """
        Run the weekly recovery pipeline

        :return: None
    """

    today = datetime.now(UTC).date()

    # Monday = 0, Sunday = 6
    current_week_start = today - timedelta(days=today.weekday())

    previous_week_start = current_week_start - timedelta(days=7)
    previous_week_end = current_week_start - timedelta(days=1)

    date_range = (
        previous_week_start.strftime("%Y-%m-%d"),
        previous_week_end.strftime("%Y-%m-%d")
    )

    collect_and_insert_features(OPENMETEO_WEATHER_URL, "BACKFILL", date_range)