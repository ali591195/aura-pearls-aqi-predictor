# URLS
OPENMETEO_AIRQUALITY_URL: str = "https://air-quality-api.open-meteo.com/v1/air-quality"
OPENMETEO_WEATHER_URL: str = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_WEATHER_HISTORICAL_URL: str = "https://archive-api.open-meteo.com/v1/archive"

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

BASELINE_FEATURES = [
    "aqi_today",
    "pm25_today",
    "pm10_today",
    "o3_today",
    "co_today",
    "no2_today",
    "so2_today",
]

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

LOG_TRANSFORM_FEATURES = [
    "co_today",
    "pm25_roll_mean_3",
    "pm25_roll_mean_7",
    "pm10_roll_std_3",
    "pm10_roll_std_7",
]

# Backfill start
HISTORICAL_BACKFILL_START_DATE = "2022-08-05"
HISTORICAL_BACKFILL_END_DATE = "2026-08-08"