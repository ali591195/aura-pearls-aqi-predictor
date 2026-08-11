# Imports
import pandas as pd

from src.feature_pipeline.data_collector import collect_features
from src.feature_pipeline.hopsworks_client import raw_hourly_fs
from src.feature_pipeline.constants import OPENMETEO_WEATHER_URL

def run_hourly_pipeline() -> None:
    """
        Run the feature pipeline

        :return: None
    """

    features = collect_features(OPENMETEO_WEATHER_URL, "HOURLY")

    if features is None:
        raise RuntimeError("Feature collection failed.")

    df = pd.DataFrame(features)

    # Insert into the feature store for raw data
    raw_hourly_fs.insert(df, write_options={"wait_for_job": True})


