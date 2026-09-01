from datetime import datetime, timezone

from backend.app.schemas.current_weather import (
    CurrentWeatherResponse,
)
from src.common.constants import OPENMETEO_WEATHER_URL
from src.common.schemas import DateRange
from src.feature_pipeline.openmeteo_client import (
    fetch_openmeteo_data,
    get_openmeteo_params,
)


def fetch_current_weather() -> CurrentWeatherResponse:
    """
    Fetch today's hourly weather data from Open-Meteo and return
    the reading for the current UTC hour.
    """

    now = datetime.now(timezone.utc)
    today = now.date()

    date_range: DateRange = (
        today.isoformat(),
        today.isoformat(),
    )

    params = get_openmeteo_params(
        date_range=date_range,
        mode="WEATHER",
    )

    response = fetch_openmeteo_data(
        url=OPENMETEO_WEATHER_URL,
        params=params,
    )

    if response is None:
        raise RuntimeError(
            "Failed to fetch today's weather data from Open-Meteo."
        )

    data = response.json()

    hourly = data.get("hourly")
    hourly_units = data.get("hourly_units")

    if not hourly or not hourly_units:
        raise RuntimeError(
            "Open-Meteo response is missing hourly weather data."
        )

    times = hourly.get("time")

    if not times:
        raise RuntimeError(
            "Open-Meteo response contains no hourly timestamps."
        )

    timestamps = [
        datetime.fromisoformat(timestamp).replace(
            tzinfo=timezone.utc
        )
        for timestamp in times
    ]

    current_hour = now.replace(
        minute=0,
        second=0,
        microsecond=0,
    )

    try:
        current_index = timestamps.index(current_hour)
    except ValueError as error:
        raise RuntimeError(
            f"Current hour {current_hour.isoformat()} "
            "was not found in the Open-Meteo response."
        ) from error

    return CurrentWeatherResponse(
        ts=timestamps[current_index],
        temperature=hourly["temperature_2m"][current_index],
        humidity=hourly["relative_humidity_2m"][current_index],
        pressure=hourly["surface_pressure"][current_index],
        wind_speed=hourly["wind_speed_10m"][current_index],
        dew_point=hourly["dew_point_2m"][current_index],
        unit_temperature=hourly_units["temperature_2m"],
        unit_humidity=hourly_units["relative_humidity_2m"],
        unit_pressure=hourly_units["surface_pressure"],
        unit_wind_speed=hourly_units["wind_speed_10m"],
        unit_dew_point=hourly_units["dew_point_2m"],
    )