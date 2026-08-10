from typing import Literal

from src.feature_pipeline.schemas import Pollutants, PollutantName, Number

# URLS
OPENMETEO_AIRQUALITY_URL: str = "https://air-quality-api.open-meteo.com/v1/air-quality"
OPENMETEO_WEATHER_URL: str = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_WEATHER_HISTORICAL_URL: str = "https://archive-api.open-meteo.com/v1/archive"

# Timeout for requests
TIMEOUT: float = 10

UNIVERSAL_GAS_CONSTANT = 8.314462618

# City Location
LAHORE_LATITUDE = 31.558
LAHORE_LONGITUDE = 74.3507

# Pollutants Constants
POLLUTANTS_MAX_CONCENTRATION: Pollutants = {
    "pm25" : 500.4,
    "pm10" : 604,
    "o3": 0.2,
    "co": 50.4,
    "no2": 2049,
    "so2": 1004,
}

POLLUTANTS_CONVERSION_DATA: dict[PollutantName, tuple[Number, Literal["ppm", "ppb"]]] = {
    "o3": (48.0, "ppm"),
    "co": (28.01, "ppm"),
    "no2": (46.01, "ppb"),
    "so2": (64.07, "ppb")
}

POLLUTANTS_BREAKPOINTS: dict[PollutantName, list[tuple[Number, Number, int, int]]] = {
    "pm25" : [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, POLLUTANTS_MAX_CONCENTRATION["pm25"], 401, 500),
    ],
    "pm10" : [
        (0.0, 54.0, 0, 50),
        (55.0, 154.0, 51, 100),
        (155.0, 254.0, 101, 150),
        (255.0, 354.0, 151, 200),
        (355.0, 424.0, 201, 300),
        (425.0, 504.0, 301, 400),
        (505.0, POLLUTANTS_MAX_CONCENTRATION["pm10"], 401, 500),
    ],
    "o3": [
        (0.000, 0.054, 0, 50),
        (0.055, 0.070, 51, 100),
        (0.071, 0.085, 101, 150),
        (0.086, 0.105, 151, 200),
        (0.106, POLLUTANTS_MAX_CONCENTRATION["o3"], 201, 300),
    ],
    "co": [
        (0.0, 4.4, 0, 50),
        (4.5, 9.4, 51, 100),
        (9.5, 12.4, 101, 150),
        (12.5, 15.4, 151, 200),
        (15.5, 30.4, 201, 300),
        (30.5, 40.4, 301, 400),
        (40.5, POLLUTANTS_MAX_CONCENTRATION["co"], 401, 500),
    ],
    "no2": [
        (0, 53, 0, 50),
        (54, 100, 51, 100),
        (101, 360, 101, 150),
        (361, 649, 151, 200),
        (650, 1249, 201, 300),
        (1250, 1649, 301, 400),
        (1650, POLLUTANTS_MAX_CONCENTRATION["no2"], 401, 500),
    ],
    "so2": [
        (0, 35, 0, 50),
        (36, 75, 51, 100),
        (76, 185, 101, 150),
        (186, 304, 151, 200),
        (305, 604, 201, 300),
        (605, 804, 301, 400),
        (805, POLLUTANTS_MAX_CONCENTRATION["so2"], 401, 500),
    ],
}
