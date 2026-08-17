from datetime import datetime, UTC

from src.common.constants import OPENMETEO_AIRQUALITY_URL
from src.common.hopsworks_client import insert_raw_features
from src.feature_pipeline.openmeteo_client import get_openmeteo_params, fetch_openmeteo_data
from src.feature_pipeline.parsers import parse_openmeteo_hour, extract_hourly_data, parse_openmeteo_hours
from src.common.schemas import FeatureDict, DateRange, CollectionMode


def collect_features(weather_api: str, mode: CollectionMode, date_range: DateRange | None = None) -> list[FeatureDict] | None:
    """
        Collect features and modify structure according to Feature Group

        :param weather_api: The weather api url.
        :param mode: Mode for collecting features.
        :param date_range: Tuple containing the start and end dates (YYYY-MM-DD).
        :return: If parser result is a list of FeatureDict, then return that otherwise None
    """

    if date_range is None:
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        date_range = (today, today)

    # Endpoints parameters
    openmeteo_airquality_params = get_openmeteo_params(date_range, "AIR_QUALITY")
    openmeteo_weather_params = get_openmeteo_params(date_range, "WEATHER")

    # Fetch pollutant data &  weather conditions for Lahore
    openmeteo_airquality_response = fetch_openmeteo_data(OPENMETEO_AIRQUALITY_URL, openmeteo_airquality_params)
    openmeteo_weather_response = fetch_openmeteo_data(weather_api, openmeteo_weather_params)

    if openmeteo_airquality_response is not None and openmeteo_weather_response is not None:
        # Get hourlies data from response
        airquality_hourly_data, weather_hourly_data = extract_hourly_data(openmeteo_airquality_response, openmeteo_weather_response)

        if airquality_hourly_data is not None and weather_hourly_data is not None:

            if mode == "HOURLY":
                ts = datetime.now(UTC).replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M")
                i = airquality_hourly_data["time"].index(ts)

                # Get features
                features = parse_openmeteo_hour(airquality_hourly_data, weather_hourly_data, i)

                if features is not None:
                    return [features]
            elif mode == "BACKFILL":
                features = parse_openmeteo_hours(airquality_hourly_data, weather_hourly_data)

                return features
            else:
                print("Please write supported modes.")

    return None

def collect_and_insert_features(weather_api: str, mode: CollectionMode, date_range: DateRange | None = None) -> None:
    """
        Collect features and insert features in feature store

        :param weather_api: The weather api url.
        :param mode: Mode for collecting features.
        :param date_range: Tuple containing the start and end dates (YYYY-MM-DD).
        :return: None
    """

    features = collect_features(weather_api, mode, date_range)

    if features is None:
        raise RuntimeError("Feature collection failed.")

    insert_raw_features(features)

