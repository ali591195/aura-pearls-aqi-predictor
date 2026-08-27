import os
import tempfile
import platform
from pathlib import Path

import pandas as pd
import hopsworks
from dotenv import load_dotenv
from hsfs.feature_group import ExternalFeatureGroup, FeatureGroup, SpineGroup

from src.common.schemas import FeatureDict, EngineeredFeatureDict

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

engineered_daily_fs = fs.get_or_create_feature_group(
    name="engineered_daily_readings",
    description="Engineered daily air quality and weather observations from Hopsworks Raw Hourly Readings Feature Store.",
    version=1,
    primary_key=["ts"],
    event_time="ts",
    online_enabled=False,
    time_travel_format="HUDI", # Default was DELTA
)

# Getting Model Registry
mr = project.get_model_registry()

def insert_features(features: list[FeatureDict] | list[EngineeredFeatureDict],
                    feature_store: FeatureGroup | ExternalFeatureGroup | SpineGroup,
                    null_columns : list[str] | None = None) -> None:
    """
        Insert the features in feature group

        :param features: List of FeatureDict
        :param feature_store: Feature Store
        :param null_columns: Columns with null values
        :return: None
    """
    df = pd.DataFrame(features)

    if null_columns:
        df[null_columns] = df[null_columns].astype("float64")

    # Insert into the feature store for raw data
    feature_store.insert(df, write_options={"wait_for_job": True})

    feature_store.get_expectation_suite()

def insert_raw_features(features: list[FeatureDict]) -> None:
    """
        Insert the features in raw hourly reading feature group

        :param features: List of FeatureDict
        :return: None
    """

    insert_features(features, raw_hourly_fs)

def insert_engineered_features(features: list[EngineeredFeatureDict], null_columns : list[str] | None = None) -> None:
    """
        Insert the features in engineered daily reading feature group

        :param features: List of FeatureDict
        :param null_columns: Columns with null values
        :return: None
    """

    insert_features(features, engineered_daily_fs, null_columns)