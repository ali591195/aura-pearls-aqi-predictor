# Imports
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, UTC
from requests import Response
from typing import TypedDict, TypeAlias

# Load environment variables
load_dotenv()

# Environment variables
AQICN_API_KEY = os.getenv("AQICN_API_KEY")
# OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# API Endpoints
AQICN_URL = "https://api.waqi.info/feed/lahore/"
# OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Timeout for requests
TIMEOUT = 10

# Endpoints parameters
aqicn_params = {
    "token": AQICN_API_KEY
}

# openweather_params = {
#     "q": "Lahore",
#     "appid": OPENWEATHER_API_KEY,
#     "units": "metric"
# }


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

def fetch_data(url: str, params: dict[str, str]) -> Response | None:
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


# Fetch current AQI & pollutant data for Lahore
aqicn_response = fetch_data(AQICN_URL, aqicn_params)

# Fetch current weather conditions for Lahore
# openweather_response = fetch_data(OPENWEATHER_URL, openweather_params)


# def format_json(json_response: object) -> str:
#     """
#         Convert a Python object into a formatted JSON string
#
#         :param json_response: Response's JSON object
#         :return: A JSON string with proper indents
#     """
#
#     return json.dumps(json_response, indent=4)


# Reusable Number type
Number: TypeAlias = float | int


# Collected feature type
class FeatureDict(TypedDict):
    aqi: Number

    pm25: Number
    pm10: Number
    o3: Number
    co: Number
    no2: Number
    so2: Number

    temp: Number
    humidity: Number
    pressure: Number
    wind_spd: Number

    ts: datetime


def parse_aqicn_response(aqicn_resp: Response) -> FeatureDict | None:
    """
        Raise status error, check header, get relevant data, print & return it

        :param aqicn_resp: Response Object
        :return: If header is application/json, then return a FeatureDict, otherwise None
    """

    # Safely check header type
    header = aqicn_resp.headers.get("Content-Type", "")
    print(f"Header: {header}")

    if "application/json" in header:
        # Get data
        data = aqicn_resp.json()["data"]
        iaqi = data["iaqi"]

        # Dictionary of required data
        fetched_data: FeatureDict = {
            "aqi": data["aqi"],

            "pm25": iaqi.get("pm25", {}).get("v", 0),
            "pm10": iaqi.get("pm10", {}).get("v", 0),
            "o3": iaqi.get("o3", {}).get("v", 0),
            "co": iaqi.get("co", {}).get("v", 0),
            "no2": iaqi.get("no2", {}).get("v", 0),
            "so2": iaqi.get("so2", {}).get("v", 0),

            "temp": iaqi.get("t", {}).get("v", 0),
            "humidity": iaqi.get("h", {}).get("v", 0),
            "pressure": iaqi.get("p", {}).get("v", 0),
            "wind_spd": iaqi.get("w", {}).get("v", 0),

            "ts": datetime.fromtimestamp(data["time"]["v"], tz=UTC)
        }

        print(f"Fetched data: {fetched_data}")

        return fetched_data

    else:
        print("The response is not json.")

        return None


if aqicn_response is not None:
    parse_aqicn_response(aqicn_response)


