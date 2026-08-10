# Imports
import pandas as pd

from src.feature_pipeline.data_collector import collect_features
from src.feature_pipeline.hopsworks_client import raw_hourly_fs
from src.feature_pipeline.constants import OPENMETEO_WEATHER_URL

def run_feature_pipeline() -> None:
    """
        Run the feature pipeline

        :return: None
    """

    features = collect_features(("2026-08-03", "2026-08-03"), OPENMETEO_WEATHER_URL)

    if features is not None:
        df = pd.DataFrame(features)

        # Insert into the feature store for raw data
        raw_hourly_fs.insert(df)


