# Imports
import os
import json
from typing import TypedDict

import requests
from dotenv import load_dotenv
from requests import Response

# Load environment variables
load_dotenv()

# Environment variables
AQICN_API_KEY = os.getenv("AQICN_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# API Endpoints
AQICN_URL = "https://api.waqi.info/feed/lahore/"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Timeout for requests
TIMEOUT = 10

# Endpoints parameters
aqicn_params = {
    "token": AQICN_API_KEY
}

openweather_params = {
    "q": "Lahore",
    "appid": OPENWEATHER_API_KEY,
    "units": "metric"
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

def fetch_data(url: str, params: dict) -> Response | None:
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
openweather_response = fetch_data(OPENWEATHER_URL, openweather_params)


def format_json(json_response: object) -> str:
    """
        Convert a Python object into a formatted JSON string

        :param json_response: Response's JSON object
        :return: A JSON string with proper indents
    """

    return json.dumps(json_response, indent=4)


def process_response(api_response: Response) -> None:
    """
        Raise status error, check header, and print response.

        :param api_response: Response Object
        :return: None
    """

    # Safely check header type
    header = api_response.headers.get("Content-Type", "")
    print(f"Header: {header}")

    if "application/json" in header:
        print(f"Json: {format_json(api_response.json())}\n")
    else:
        print("The response is not json.")


# An array of responses
responses = [aqicn_response, openweather_response]

for response in responses:
    if response is not None:
        process_response(response)
