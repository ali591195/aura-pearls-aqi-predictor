import subprocess
from pathlib import Path

# URLS
OPENMETEO_AIRQUALITY_URL: str = "https://air-quality-api.open-meteo.com/v1/air-quality"
OPENMETEO_WEATHER_URL: str = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_WEATHER_HISTORICAL_URL: str = "https://archive-api.open-meteo.com/v1/archive"

AIR_QUALITY_PARAMS = ["pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "us_aqi"]
WEATHER_PARAMS = ["temperature_2m", "dew_point_2m", "relative_humidity_2m", "surface_pressure", "wind_speed_10m"]

# Timeout for requests
TIMEOUT: float = 10

# City Location
LAHORE_LATITUDE = 31.558
LAHORE_LONGITUDE = 74.3507

# Target columns for model
TARGET_COLUMNS = [
        "target_aqi_day1",
        "target_aqi_day2",
        "target_aqi_day3",
        "target_aqi_day4",
]

# Feature extraction baseline
BASELINE_FEATURES = [
    "aqi_today",
    "pm25_today",
    "pm10_today",
    "o3_today",
    "co_today",
    "no2_today",
    "so2_today",
]

# Feature extraction finalized features
FINAL_SELECTED_FEATURES = [
    "pm25_today",
    "pm10_today",
    "o3_today",
    "co_today",
    "no2_today",
    "so2_today",
    "aqi_roll_mean_7",

    "pm25_lag_1",
    "pm25_lag_2",
    "pm25_lag_3",
    "pm25_roll_mean_3",
    "pm25_roll_mean_7",
    "pm25_roll_std_3",
    "pm25_roll_std_7",

    "pm10_roll_mean_7",
    "pm10_roll_std_3",
    "pm10_roll_std_7",

    "o3_lag_1",
    "o3_lag_2",
    "o3_roll_mean_3",
    "o3_roll_mean_7",
    "o3_roll_std_3",

    "month",
]

# Rightly skewed features from feature extraction finalized features
LOG_TRANSFORM_FEATURES = [
    "co_today",
    "pm25_roll_mean_3",
    "pm25_roll_mean_7",
    "pm10_roll_std_3",
    "pm10_roll_std_7",
]

# All training features
ALL_TRAINING_FEATURES = [
    "aqi_today",
    "aqi_lag_1",
    "aqi_lag_2",
    "aqi_lag_3",
    "aqi_roll_mean_3",
    "aqi_roll_mean_7",
    "aqi_roll_std_3",
    "aqi_roll_std_7",
    "pm25_today",
    "pm25_lag_1",
    "pm25_lag_2",
    "pm25_lag_3",
    "pm25_roll_mean_3",
    "pm25_roll_mean_7",
    "pm25_roll_std_3",
    "pm25_roll_std_7",
    "pm10_today",
    "pm10_lag_1",
    "pm10_lag_2",
    "pm10_lag_3",
    "pm10_roll_mean_3",
    "pm10_roll_mean_7",
    "pm10_roll_std_3",
    "pm10_roll_std_7",
    "o3_today",
    "o3_lag_1",
    "o3_lag_2",
    "o3_lag_3",
    "o3_roll_mean_3",
    "o3_roll_mean_7",
    "o3_roll_std_3",
    "o3_roll_std_7",
    "temp_today",
    "temp_lag_1",
    "humidity_today",
    "humidity_lag_1",
    "wind_spd_today",
    "wind_spd_lag_1",
    "pressure_today",
    "pressure_lag_1",
    "dew_pt_today",
    "dew_pt_lag_1",
    "co_today",
    "so2_today",
    "no2_today",
    "day_of_week",
    "is_weekend",
    "month",
    "aqi_change_rate",
]

# All skewed features
ALL_LOG_TRANSFORM_FEATURES = [
    "aqi_roll_std_3",
    "aqi_roll_std_7",
    "co_today",
    "pm25_roll_mean_3",
    "pm25_roll_mean_7",
    "pm10_roll_std_3",
    "pm10_roll_std_7",
]

# Selected feature sets for each day
SELECTED_FEATURES_TARGET_1 = [
    "aqi_today",
    "aqi_lag_1",
    "aqi_lag_2",
    "aqi_roll_mean_7",

    "pm25_today",
    "pm25_lag_1",
    "pm25_roll_mean_3",
    "pm25_roll_mean_7",
    "pm25_roll_std_3",

    "pm10_today",
    "pm10_lag_1",
    "pm10_lag_2",
    "pm10_lag_3",
    "pm10_roll_mean_3",
    "pm10_roll_mean_7",
    "pm10_roll_std_3",

    "o3_today",
    "o3_lag_1",
    "o3_lag_2",
    "o3_roll_mean_3",
    "o3_roll_mean_7",

    "temp_today",
    "wind_spd_today",

    "co_today",
    "so2_today",
    "no2_today",
]
SELECTED_FEATURES_TARGET_2 = [
  "aqi_today",
  "aqi_lag_1",
  "aqi_lag_2",
  "aqi_lag_3",
  "aqi_roll_mean_3",
  "aqi_roll_mean_7",

  "pm25_today",
  "pm25_lag_1",
  "pm25_lag_2",
  "pm25_lag_3",
  "pm25_roll_mean_7",

  "o3_today",
  "o3_lag_1",
  "o3_lag_2",
  "o3_roll_mean_7",

  "pm10_today",
  "pm10_lag_1",
  "pm10_roll_mean_7",

  "co_today",
  "so2_today",
  "no2_today",

  "temp_today",
  "temp_lag_1",
]
SELECTED_FEATURES_TARGET_3 = [
  "aqi_today",
  "aqi_lag_1",
  "aqi_lag_2",
  "aqi_lag_3",
  "aqi_roll_mean_7",

  "pm25_today",
  "pm25_lag_1",
  "pm25_lag_2",
  "pm25_lag_3",
  "pm25_roll_mean_7",

  "o3_today",
  "o3_lag_1",
  "o3_lag_2",
  "o3_lag_3",
  "o3_roll_mean_7",

  "pm10_today",
  "pm10_lag_1",
  "pm10_lag_2",
  "pm10_lag_3",
  "pm10_roll_mean_7",

  "co_today",
  "so2_today",
  "no2_today",

  "temp_today",
  "temp_lag_1",
]
SELECTED_FEATURES_TARGET_4 = [
  "aqi_today",
  "aqi_lag_1",
  "aqi_lag_2",
  "aqi_lag_3",
  "aqi_roll_mean_7",

  "pm25_today",
  "pm25_lag_1",
  "pm25_lag_2",
  "pm25_lag_3",
  "pm25_roll_mean_7",

  "o3_today",
  "o3_lag_1",
  "o3_lag_2",
  "o3_lag_3",
  "o3_roll_mean_7",

  "pm10_today",
  "pm10_lag_1",
  "pm10_lag_2",
  "pm10_lag_3",
  "pm10_roll_mean_7",

  "co_today",
  "so2_today",
  "no2_today",

  "temp_today",
  "temp_lag_1",

  "dew_pt_today",
  "dew_pt_lag_1",
]

SELECTED_FEATURES_LIST = [
    SELECTED_FEATURES_TARGET_1,
    SELECTED_FEATURES_TARGET_2,
    SELECTED_FEATURES_TARGET_3,
    SELECTED_FEATURES_TARGET_4
]

LATEST_SELECTED_FEATURES_TARGET_1 = [
    'aqi_today',
    'pm25_today',
    'pm10_today',
    'o3_today',
    'no2_today',
    'temp_today',
    'wind_spd_today',
    'dew_pt_today',
    'pm25_lag_1',
    'pm25_lag_2',
    'pm10_lag_3',
    'temp_lag_1',
    'pressure_lag_1',
    'humidity_lag_1',
    'pm25_roll_mean_3',
    'o3_roll_mean_3',
    'pm25_roll_std_3',
    'o3_roll_std_3'
]
LATEST_SELECTED_FEATURES_TARGET_2 = [
    'pm25_today',
    'pm10_today',
    'o3_today',
    'co_today',
    'no2_today',
    'so2_today',
    'temp_today',
    'pressure_today',
    'humidity_today',
    'wind_spd_today',
    'dew_pt_today',
    'pm10_lag_1',
    'o3_lag_1',
    'pm25_lag_2',
    'pm10_lag_2',
    'o3_lag_2',
    'pm25_lag_3',
    'pm10_lag_3',
    'o3_lag_3',
    'temp_lag_1',
    'pressure_lag_1',
    'humidity_lag_1',
    'wind_spd_lag_1',
    'dew_pt_lag_1',
    'pm25_roll_mean_3',
    'pm25_roll_mean_7',
    'pm10_roll_mean_3',
    'pm10_roll_mean_7',
    'o3_roll_mean_3',
    'o3_roll_mean_7',
    'pm25_roll_std_3',
    'pm25_roll_std_7',
    'pm10_roll_std_3',
    'pm10_roll_std_7',
    'o3_roll_std_3',
    'o3_roll_std_7',
    'day_of_week',
    'month'
]
LATEST_SELECTED_FEATURES_TARGET_3 = ALL_TRAINING_FEATURES
LATEST_SELECTED_FEATURES_TARGET_4 = ALL_TRAINING_FEATURES

LATEST_SELECTED_FEATURES_LIST = [
    LATEST_SELECTED_FEATURES_TARGET_1,
    LATEST_SELECTED_FEATURES_TARGET_2,
    LATEST_SELECTED_FEATURES_TARGET_3,
    LATEST_SELECTED_FEATURES_TARGET_4
]

CURRENT_PROD_MODELS = [
    ("aqi_xgboost_day_1", "XGBoost"),
    ("aqi_mlp_day_2", "MLP"),
    ("aqi_lightgbm_day_3", "LightGBM"),
    ("aqi_rf_day_4", "Random Forest"),
]

# Backfill start
HISTORICAL_BACKFILL_START_DATE = "2022-08-05"
HISTORICAL_BACKFILL_END_DATE = "2026-08-08"

# Root directory
# New: derive root from this file's own location, no subprocess needed
ROOT_DIR = Path(__file__).resolve().parents[2]

# Model storing directory
MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)