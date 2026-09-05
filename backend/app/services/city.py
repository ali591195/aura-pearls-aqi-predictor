from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

from backend.app.schemas.city import CityResponse
from backend.app.schemas.current_air_quality import (
    CurrentAirQualityResponse,
)
from backend.app.schemas.current_weather import (
    CurrentWeatherResponse,
)
from backend.app.schemas.prediction import (
    AQIPredictionResponse,
)
from backend.app.services.model_service import (
    get_models,
    get_scaler,
)
from src.common.constants import (
    ALL_LOG_TRANSFORM_FEATURES,
    ALL_TRAINING_FEATURES,
    LATEST_SELECTED_FEATURES_LIST,
    OPENMETEO_AIRQUALITY_URL,
    OPENMETEO_WEATHER_URL,
)
from src.common.schemas import DateRange
from src.engineered_features.data_utils import (
    build_daily_engineered_features,
)
from src.feature_pipeline.openmeteo_client import (
    fetch_openmeteo_data,
    get_openmeteo_params,
)
from src.feature_pipeline.parsers import (
    parse_openmeteo_hour,
)


def _get_prediction_date() -> datetime:
    """
    Get yesterday as a UTC datetime.
    """

    yesterday = (
        datetime.now(timezone.utc).date()
        - timedelta(days=1)
    )

    return datetime.combine(
        yesterday,
        datetime.min.time(),
        tzinfo=timezone.utc,
    )


def _get_date_range() -> DateRange:
    """
    Get the seven completed days ending yesterday.

    Today is intentionally excluded.
    """

    yesterday = (
        datetime.now(timezone.utc).date()
        - timedelta(days=1)
    )

    start_date = yesterday - timedelta(days=6)

    return (
        start_date.isoformat(),
        yesterday.isoformat(),
    )


def _get_today_date_range() -> DateRange:
    """
    Get today's date for current city data.
    """

    today = datetime.now(timezone.utc).date()

    return (
        today.isoformat(),
        today.isoformat(),
    )


def _get_openmeteo_params(
    latitude: float,
    longitude: float,
    date_range: DateRange,
    mode: str,
) -> dict:
    """
    Build Open-Meteo parameters for the requested coordinates.
    """

    params = get_openmeteo_params(
        date_range=date_range,
        mode=mode,
    )

    params["latitude"] = latitude
    params["longitude"] = longitude

    return params


def _fetch_city_raw_features(
    latitude: float,
    longitude: float,
    date_range: DateRange,
) -> list[dict]:
    """
    Fetch seven days of hourly air-quality and weather data
    and convert the response into raw feature-store format.
    """

    air_quality_params = _get_openmeteo_params(
        latitude=latitude,
        longitude=longitude,
        date_range=date_range,
        mode="AIR_QUALITY",
    )

    weather_params = _get_openmeteo_params(
        latitude=latitude,
        longitude=longitude,
        date_range=date_range,
        mode="WEATHER",
    )

    air_quality_response = fetch_openmeteo_data(
        url=OPENMETEO_AIRQUALITY_URL,
        params=air_quality_params,
    )

    if air_quality_response is None:
        raise RuntimeError(
            "Failed to fetch air-quality data from Open-Meteo."
        )

    weather_response = fetch_openmeteo_data(
        url=OPENMETEO_WEATHER_URL,
        params=weather_params,
    )

    if weather_response is None:
        raise RuntimeError(
            "Failed to fetch weather data from Open-Meteo."
        )

    air_quality_data = air_quality_response.json()
    weather_data = weather_response.json()

    air_quality_hourly = air_quality_data.get("hourly")
    weather_hourly = weather_data.get("hourly")

    if not air_quality_hourly:
        raise RuntimeError(
            "Open-Meteo response is missing hourly "
            "air-quality data."
        )

    if not weather_hourly:
        raise RuntimeError(
            "Open-Meteo response is missing hourly "
            "weather data."
        )

    air_quality_times = air_quality_hourly.get("time")
    weather_times = weather_hourly.get("time")

    if not air_quality_times:
        raise RuntimeError(
            "Open-Meteo response contains no hourly "
            "air-quality timestamps."
        )

    if not weather_times:
        raise RuntimeError(
            "Open-Meteo response contains no hourly "
            "weather timestamps."
        )

    if len(air_quality_times) != len(weather_times):
        raise RuntimeError(
            "Air-quality and weather responses contain "
            "different numbers of hourly readings."
        )

    features = []

    for i in range(len(air_quality_times)):
        feature = parse_openmeteo_hour(
            airquality_hourly_data=air_quality_hourly,
            weather_hourly_data=weather_hourly,
            i=i,
        )

        if feature is not None:
            features.append(feature)

    if not features:
        raise RuntimeError(
            "No valid raw features could be created "
            "from the Open-Meteo response."
        )

    return features


def _fetch_current_air_quality(
    latitude: float,
    longitude: float,
) -> CurrentAirQualityResponse:
    """
    Fetch today's current air-quality reading and
    today's AQI mean for the requested coordinates.
    """

    now = datetime.now(timezone.utc)
    today = now.date()

    date_range: DateRange = (
        today.isoformat(),
        today.isoformat(),
    )

    params = _get_openmeteo_params(
        latitude=latitude,
        longitude=longitude,
        date_range=date_range,
        mode="AIR_QUALITY",
    )

    response = fetch_openmeteo_data(
        url=OPENMETEO_AIRQUALITY_URL,
        params=params,
    )

    if response is None:
        raise RuntimeError(
            "Failed to fetch today's air-quality data "
            "from Open-Meteo."
        )

    data = response.json()

    hourly = data.get("hourly")
    hourly_units = data.get("hourly_units")

    if not hourly or not hourly_units:
        raise RuntimeError(
            "Open-Meteo response is missing hourly "
            "air-quality data."
        )

    times = hourly.get("time")

    if not times:
        raise RuntimeError(
            "Open-Meteo response contains no hourly "
            "air-quality timestamps."
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

    today_aqi_mean = (
        sum(current_aqi_values)
        / len(current_aqi_values)
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


def _fetch_current_weather(
    latitude: float,
    longitude: float,
) -> CurrentWeatherResponse:
    """
    Fetch today's current weather reading for
    the requested coordinates.
    """

    now = datetime.now(timezone.utc)
    today = now.date()

    date_range: DateRange = (
        today.isoformat(),
        today.isoformat(),
    )

    params = _get_openmeteo_params(
        latitude=latitude,
        longitude=longitude,
        date_range=date_range,
        mode="WEATHER",
    )

    response = fetch_openmeteo_data(
        url=OPENMETEO_WEATHER_URL,
        params=params,
    )

    if response is None:
        raise RuntimeError(
            "Failed to fetch today's weather data "
            "from Open-Meteo."
        )

    data = response.json()

    hourly = data.get("hourly")
    hourly_units = data.get("hourly_units")

    if not hourly or not hourly_units:
        raise RuntimeError(
            "Open-Meteo response is missing hourly "
            "weather data."
        )

    times = hourly.get("time")

    if not times:
        raise RuntimeError(
            "Open-Meteo response contains no hourly "
            "weather timestamps."
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


def _get_predictions(
    prediction_df: pd.DataFrame,
) -> list[np.ndarray]:
    """
    Generate predictions using the production models.
    """

    models = get_models()
    scaler = get_scaler()

    predictions = []

    df_preprocess = prediction_df.copy()

    for feature in ALL_LOG_TRANSFORM_FEATURES:
        df_preprocess[feature] = np.log1p(
            df_preprocess[feature]
        )

    df_preprocess[ALL_TRAINING_FEATURES] = (
        scaler.transform(
            df_preprocess[ALL_TRAINING_FEATURES]
        )
    )

    for i, feature_list in enumerate(
        LATEST_SELECTED_FEATURES_LIST
    ):
        model, model_type = models[i]

        if model_type == "MLP":
            prediction = model.predict(
                df_preprocess[feature_list]
            )
        else:
            prediction = model.predict(
                prediction_df[feature_list]
            )

        predictions.append(
            prediction.flatten()
        )

    return predictions


def get_city_prediction(
    latitude: float,
    longitude: float,
) -> CityResponse:
    """
    Generate the complete city response.

    Predictions use the seven completed days ending yesterday.
    Today's air-quality and weather data are returned separately
    as current city information.
    """

    date_range = _get_date_range()

    raw_features = _fetch_city_raw_features(
        latitude=latitude,
        longitude=longitude,
        date_range=date_range,
    )

    df = pd.DataFrame(raw_features)

    df["ts"] = pd.to_datetime(
        df["ts"],
        utc=True,
    )

    prediction_date = _get_prediction_date()

    engineered_features = (
        build_daily_engineered_features(
            df=df,
            date=prediction_date,
        )
    )

    prediction_df = pd.DataFrame(
        [engineered_features]
    )

    predictions = _get_predictions(
        prediction_df=prediction_df,
    )

    prediction = AQIPredictionResponse(
        aqi_pred_day_1=float(predictions[0][0]),
        aqi_pred_day_2=float(predictions[1][0]),
        aqi_pred_day_3=float(predictions[2][0]),
        aqi_pred_day_4=float(predictions[3][0]),
        ts=prediction_date,
    )

    current_air_quality = _fetch_current_air_quality(
        latitude=latitude,
        longitude=longitude,
    )

    current_weather = _fetch_current_weather(
        latitude=latitude,
        longitude=longitude,
    )

    return CityResponse(
        prediction=prediction,
        current_air_quality=current_air_quality,
        current_weather=current_weather,
    )