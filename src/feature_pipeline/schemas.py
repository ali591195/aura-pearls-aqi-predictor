from typing import TypedDict, Literal

from datetime import datetime

# Reusable Number type
type Number = float | int

type PollutantName = Literal["pm25", "pm10", "o3", "co", "no2", "so2"]


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