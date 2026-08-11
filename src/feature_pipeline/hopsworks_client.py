import os
import tempfile
import platform
from pathlib import Path

import pandas as pd
import hopsworks
from dotenv import load_dotenv

from src.feature_pipeline.schemas import FeatureDict

# Load environment variable
load_dotenv()

# Login Parameters
login_kwargs = {
    "api_key_value": os.getenv("HOPSWORKS_API_KEY"),
    "project": "aura_pearls_aqi_predictor", # Name
}

if platform.system() == "Windows":
    login_kwargs["cert_folder"] = str(Path(tempfile.gettempdir()) / "hopsworks_certs") # Overriding the linux file paths

# Get project from hopsworks system
project = hopsworks.login(**login_kwargs)

# Getting Feature Store
fs = project.get_feature_store()

# Getting the specific feature store for raw data
raw_hourly_fs = fs.get_or_create_feature_group(
    name="raw_hourly_readings",
    description="Raw hourly air quality and weather observations from Open-Meteo.",
    version=1,
    primary_key=["ts"],
    event_time="ts",
    online_enabled=False,
    time_travel_format="HUDI" # Default was DELTA
)

def insert_raw_hourly_features(features: list[FeatureDict]) -> None:
    """
        Insert the features in feature group

        :param features: List of FeatureDict
        :return: None
    """

    df = pd.DataFrame(features)

    # Insert into the feature store for raw data
    raw_hourly_fs.insert(df, write_options={"wait_for_job": True})