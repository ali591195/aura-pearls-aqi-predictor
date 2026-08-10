from src.feature_pipeline.constants import OPENMETEO_AIRQUALITY_URL
from src.feature_pipeline.openmeteo_client import get_openmeteo_params, fetch_openmeteo_data
from src.feature_pipeline.parsers import parse_openmeteo_response
from src.feature_pipeline.schemas import FeatureDict, DateRange


def collect_features(date_range: DateRange, weather_api: str) -> list[FeatureDict] | None:
    """
        Collect features and modify structure according to Feature Group

        :param date_range: Tuple containing the start and end dates (YYYY-MM-DD).
        :param weather_api: The weather api url.
        :return: If parser result is a list of FeatureDict, then return that otherwise None
    """

    # Endpoints parameters
    openmeteo_airquality_params = get_openmeteo_params(date_range, "AIR_QUALITY")
    openmeteo_weather_params = get_openmeteo_params(date_range, "WEATHER")

    # Fetch historical pollutant data & current weather conditions for Lahore
    openmeteo_airquality_response = fetch_openmeteo_data(OPENMETEO_AIRQUALITY_URL, openmeteo_airquality_params)
    openmeteo_weather_response = fetch_openmeteo_data(weather_api, openmeteo_weather_params)

    if openmeteo_airquality_response is not None and openmeteo_weather_response is not None:
        # Get features
        features = parse_openmeteo_response(openmeteo_airquality_response, openmeteo_weather_response)

        return features

    return None
