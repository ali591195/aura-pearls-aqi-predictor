from datetime import date
from dateutil.relativedelta import relativedelta

from src.common.constants import OPENMETEO_WEATHER_HISTORICAL_URL, HISTORICAL_BACKFILL_START_DATE, \
    HISTORICAL_BACKFILL_END_DATE
from src.feature_pipeline.data_collector import collect_features
from src.common.hopsworks_client import insert_raw_features
from src.common.schemas import FeatureDict, DateRanges


def run_historical_backfill(historical_backfill_dates: DateRanges | None = None) -> None:
    """
        Run the historical backfill pipeline

        :param historical_backfill_dates: List of date ranges
        :return: None
    """

    if historical_backfill_dates is None:
        historical_backfill_dates: DateRanges = generate_backfill_date_ranges(HISTORICAL_BACKFILL_START_DATE, HISTORICAL_BACKFILL_END_DATE)

    historical_backfill_features: list[FeatureDict] = []

    # For each date range
    for date_range in historical_backfill_dates:
        features = collect_features(OPENMETEO_WEATHER_HISTORICAL_URL, "BACKFILL", date_range)

        if features is not None:
            historical_backfill_features.extend(features)

    insert_raw_features(historical_backfill_features)

def generate_backfill_date_ranges(start_date: str, end_date: str) -> DateRanges:
    """
        Generate date ranges for backfill

        :param start_date: Start date of the range
        :param end_date: End date of the range
        :return: None
    """

    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    ranges: DateRanges = []
    current_start = start

    while current_start <= end:
        next_start = current_start + relativedelta(months=3)
        current_end = min(next_start - relativedelta(days=1), end)

        ranges.append((
            current_start.isoformat(),
            current_end.isoformat(),
        ))

        current_start = current_end + relativedelta(days=1)

    return ranges