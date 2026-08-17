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

# Backfill start
HISTORICAL_BACKFILL_START_DATE = "2025-11-08"