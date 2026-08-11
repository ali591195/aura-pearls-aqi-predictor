# Imports
from src.feature_pipeline.data_collector import collect_and_insert_features
from src.feature_pipeline.constants import OPENMETEO_WEATHER_URL

def run_hourly_pipeline() -> None:
    """
        Run the hourly pipeline

        :return: None
    """

    collect_and_insert_features(OPENMETEO_WEATHER_URL, "HOURLY")


