from typing import TypedDict, Literal

from datetime import datetime

from pandas import DataFrame

# Reusable Number type
type Number = float | int

type DateRange = tuple[str, str]

type DateRanges = list[DateRange]

type CollectionMode = Literal["BACKFILL", "HOURLY"]

type FeatureEngineeringMode = Literal["WEEKLY_RECOVERY", "MONTHLY_RECOVERY", "NORMAL", "BACKFILL"]

class AirQualityHourly(TypedDict):
    time: list[str]
    us_aqi: list[float]
    pm2_5: list[float]
    pm10: list[float]
    ozone: list[float]
    carbon_monoxide: list[float]
    nitrogen_dioxide: list[float]
    sulphur_dioxide: list[float]


class WeatherHourly(TypedDict):
    time: list[str]
    temperature_2m: list[float]
    surface_pressure: list[float]
    relative_humidity_2m: list[float]
    wind_speed_10m: list[float]
    dew_point_2m: list[float]

# Collected feature type
class FeatureDict(TypedDict):
    aqi: Number

    pm25: Number
    pm10: Number
    o3: Number
    co: Number
    no2: Number
    so2: Number

    temp: Number
    pressure: Number
    humidity: Number
    wind_spd: Number
    dew_pt: Number

    ts: datetime

class EngineeredFeatureDict(TypedDict):
    # Primany Features
    aqi_today: Number
    aqi_lag_1: Number
    aqi_lag_2: Number
    aqi_lag_3: Number
    aqi_roll_mean_3: Number
    aqi_roll_mean_7: Number
    aqi_roll_std_3: Number
    aqi_roll_std_7: Number

    pm25_today: Number
    pm25_lag_1: Number
    pm25_lag_2: Number
    pm25_lag_3: Number
    pm25_roll_mean_3: Number
    pm25_roll_mean_7: Number
    pm25_roll_std_3: Number
    pm25_roll_std_7: Number

    pm10_today: Number
    pm10_lag_1: Number
    pm10_lag_2: Number
    pm10_lag_3: Number
    pm10_roll_mean_3: Number
    pm10_roll_mean_7: Number
    pm10_roll_std_3: Number
    pm10_roll_std_7: Number

    o3_today: Number
    o3_lag_1: Number
    o3_lag_2: Number
    o3_lag_3: Number
    o3_roll_mean_3: Number
    o3_roll_mean_7: Number
    o3_roll_std_3: Number
    o3_roll_std_7: Number

    # Secondary Features
    temp_today: Number
    temp_lag_1: Number

    humidity_today: Number
    humidity_lag_1: Number

    wind_spd_today: Number
    wind_spd_lag_1: Number

    pressure_today: Number
    pressure_lag_1: Number

    dew_pt_today: Number
    dew_pt_lag_1: Number

    # Minor Features
    co_today: Number
    so2_today: Number
    no2_today: Number

    # Calendar Features
    day_of_week: int
    is_weekend: bool
    month: int

    aqi_change_rate: Number

    # Target Features
    target_aqi_day1: Number | None
    target_aqi_day2: Number | None
    target_aqi_day3: Number | None
    target_aqi_day4: Number | None

    # Metadata
    ts: datetime

class DeepLearningFitParamSchema(TypedDict):
    epochs: int
    batch_size: int
    callbacks: list
    verbose: int
