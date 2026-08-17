from typing import Literal, TypedDict

from src.common.schemas import Number


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