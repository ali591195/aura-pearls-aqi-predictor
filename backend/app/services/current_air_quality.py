from datetime import datetime, timezone

from backend.app.schemas.current_air_quality import (
    CurrentAirQualityResponse,
)
from src.common.constants import OPENMETEO_AIRQUALITY_URL
from src.common.schemas import DateRange
from src.feature_pipeline.openmeteo_client import (
    fetch_openmeteo_data,
    get_openmeteo_params,
)


def fetch_current_air_quality() -> CurrentAirQualityResponse:
    """
    Fetch today's hourly air-quality data from Open-Meteo and return
    the current hourly reading together with today's AQI mean.
    """

    now = datetime.now(timezone.utc)
    today = now.date()

    date_range: DateRange = (
        today.isoformat(),
        today.isoformat(),
    )

    params = get_openmeteo_params(
        date_range=date_range,
        mode="AIR_QUALITY",
    )

    response = fetch_openmeteo_data(
        url=OPENMETEO_AIRQUALITY_URL,
        params=params,
    )

    if response is None:
        raise RuntimeError(
            "Failed to fetch today's air-quality data from Open-Meteo."
        )

    data = response.json()

    hourly = data.get("hourly")
    hourly_units = data.get("hourly_units")

    if not hourly or not hourly_units:
        raise RuntimeError(
            "Open-Meteo response is missing hourly air-quality data."
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

    current_aqi_values = [
        value
        for index, value in enumerate(hourly["us_aqi"])
        if timestamps[index] <= current_hour
        and value is not None
    ]

    if not current_aqi_values:
        raise RuntimeError(
            "No AQI readings are available for today's mean."
        )

    print(current_aqi_values)

    today_aqi_mean = sum(current_aqi_values) / len(
        current_aqi_values
    )

    return CurrentAirQualityResponse(
        ts=timestamps[current_index],
        us_aqi=hourly["us_aqi"][current_index],
        today_us_aqi_mean=today_aqi_mean,
        pm10=hourly["pm10"][current_index],
        pm2_5=hourly["pm2_5"][current_index],
        carbon_monoxide=hourly["carbon_monoxide"][current_index],
        nitrogen_dioxide=hourly["nitrogen_dioxide"][current_index],
        sulphur_dioxide=hourly["sulphur_dioxide"][current_index],
        ozone=hourly["ozone"][current_index],
        unit_pm10=hourly_units["pm10"],
        unit_pm2_5=hourly_units["pm2_5"],
        unit_carbon_monoxide=hourly_units[
            "carbon_monoxide"
        ],
        unit_nitrogen_dioxide=hourly_units[
            "nitrogen_dioxide"
        ],
        unit_sulphur_dioxide=hourly_units[
            "sulphur_dioxide"
        ],
        unit_ozone=hourly_units["ozone"],
    )