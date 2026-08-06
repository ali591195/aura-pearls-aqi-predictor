import os
import tempfile
from pathlib import Path

import hopsworks
from dotenv import load_dotenv

# Load environment variable
load_dotenv()

# Get project from hopsworks system
project = hopsworks.login(
    api_key_value=os.getenv("HOPSWORKS_API_KEY"),
    project="aura_pearls_aqi_predictor", # Name
    cert_folder=str(Path(tempfile.gettempdir()) / "hopsworks_certs") # Overriding the linux file paths
)

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