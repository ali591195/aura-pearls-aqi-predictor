# Imports
import requests
import pandas as pd
from requests import Response

from src.feature_pipeline.hopsworks_client import raw_hourly_fs
from src.feature_pipeline.parsers import parse_openmeteo_response
from src.feature_pipeline.constants import OPENMETEO_AIRQUALITY_URL, OPENMETEO_WEATHER_URL, TIMEOUT


def get_openmeteo_params(hourly: list[str]) -> dict[str, str | list[str] | float]:
    """
        Give params for open-meteo api request

        :param hourly: Hourly params list
        :return: Request params
    """

    return {
	"latitude": 31.558,
	"longitude": 74.3507,
	"hourly": hourly,
	"start_date": "2026-08-03",
	"end_date": "2026-08-03",
}


# Endpoints parameters
openmeteo_airquality_params = get_openmeteo_params(["pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone"])
openmeteo_weather_params = get_openmeteo_params(["temperature_2m", "dew_point_2m", "relative_humidity_2m", "surface_pressure", "wind_speed_10m"])


def get_exception_detail(url: str, error: requests.exceptions.RequestException) -> dict[str, str]:
    """
        Return a formatted error object

        :param url: The url endpoint
        :param error: The raised exception
        :return: A formatted error object
    """

    error_details = {
        "url": url,
        "type": error.__class__.__name__,
        "message": str(error)
    }

    if error.response is not None:
        error_details["response"] = error.response.text

    return error_details


def fetch_data(url: str, params: dict[str, str | list[str] | float]) -> Response | None:
    """
        Fetch data from the given url

        :param url: The url endpoint
        :param params: The url parameters
        :return: A Response object or none if exception is raised
    """
    try:
        resp = requests.get(url, params=params, timeout=TIMEOUT)

        # Raise status errors
        resp.raise_for_status()

        return resp

    except requests.exceptions.RequestException as e:
        print(get_exception_detail(url, e))
        return None


# Fetch current pollutant data & current weather conditions for Lahore
openmeteo_airquality_response = fetch_data(OPENMETEO_AIRQUALITY_URL, openmeteo_airquality_params)
openmeteo_weather_response = fetch_data(OPENMETEO_WEATHER_URL, openmeteo_weather_params)

if openmeteo_airquality_response is not None and openmeteo_weather_response is not None:
    # Get features
    features = parse_openmeteo_response(openmeteo_airquality_response, openmeteo_weather_response)
    df = pd.DataFrame([features])

    # Insert into the feature store for raw data
    raw_hourly_fs.insert(df)


