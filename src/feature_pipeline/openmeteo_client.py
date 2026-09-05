import time
from typing import Literal

import requests
from requests import Response

from src.common.constants import LAHORE_LATITUDE, LAHORE_LONGITUDE, TIMEOUT, AIR_QUALITY_PARAMS, WEATHER_PARAMS
from src.common.schemas import DateRange


def get_openmeteo_params(date_range: DateRange, mode: Literal["AIR_QUALITY", "WEATHER"]) -> dict[str, float | list[str] | str]:
    """
        Build request parameters for the Open-Meteo API.

        :param date_range: Tuple containing the start and end dates (YYYY-MM-DD).
        :param mode: Selects either the Air Quality or Weather endpoint parameters.
        :return: Dictionary of request parameters for the Open-Meteo API.
    """

    # Hourly parameter per mode
    air_quality_hour_params = AIR_QUALITY_PARAMS
    weather_hour_params = WEATHER_PARAMS

    # Dates extraction
    start_date, end_date = date_range

    return {
        "latitude": LAHORE_LATITUDE,
        "longitude": LAHORE_LONGITUDE,
        "hourly": air_quality_hour_params if mode == "AIR_QUALITY" else weather_hour_params,
        "start_date": start_date,
        "end_date": end_date,
    }

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

def fetch_openmeteo_data(url: str, params: dict[str, str | list[str] | float]) -> Response | None:
    """
        Fetch data from the given URL with retries.

        :param url: The url endpoint
        :param params: The url parameters
        :return: A Response object or none if exception is raised
    """
    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.get(url, params=params, timeout=TIMEOUT)

            # Raise status errors
            resp.raise_for_status()

            return resp

        except requests.exceptions.RequestException as e:
            print(f"Open-meteo request failed | attempts: {attempt}/{max_attempts}")
            print(get_exception_detail(url, e))

            if attempt < max_attempts:
                time.sleep(2 ** attempt)

    print("All Open-Meteo request attempts failed.")
    return None