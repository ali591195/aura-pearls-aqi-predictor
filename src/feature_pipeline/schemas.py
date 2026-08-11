from typing import TypedDict, Literal

from datetime import datetime

# Reusable Number type
type Number = float | int

type PollutantName = Literal["pm25", "pm10", "o3", "co", "no2", "so2"]

type DateRange = tuple[str, str]

type DateRanges = list[DateRange]

type CollectionMode = Literal["BACKFILL", "HOURLY"]

class AirQualityHourly(TypedDict):
    time: list[str]
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

class Pollutants(TypedDict):
    pm25: Number
    pm10: Number
    o3: Number
    co: Number
    no2: Number
    so2: Number


class IdealGasParams(TypedDict):
    temp: Number
    pressure: Number


# Collected feature type
class FeatureDict(Pollutants, IdealGasParams):
    aqi: Number

    humidity: Number
    wind_spd: Number
    dew_pt: Number

    ts: datetime