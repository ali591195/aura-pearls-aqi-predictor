from datetime import datetime, UTC
from requests import Response

from src.feature_pipeline.aqi import calculate_pollutants_aqis
from src.feature_pipeline.schemas import FeatureDict, Pollutants, IdealGasParams


def parse_openmeteo_response(airquality_resp: Response, weather_resp: Response) -> FeatureDict | None:
    """
        Raise status error, check header, get relevant data, print & return it

        :param airquality_resp: Air Quality API Response
        :param weather_resp: Weather API Response
        :return: If header is application/json, then return a FeatureDict, otherwise None
    """

    # Safely check header type
    airquality_header = airquality_resp.headers.get("Content-Type", "")

    weather_header = weather_resp.headers.get("Content-Type", "")

    if "application/json" in airquality_header and "application/json" in weather_header:
        # Get data
        airquality_hourly_data = airquality_resp.json()["hourly"]
        weather_hourly_data = weather_resp.json()["hourly"]

        # Dictionary of required data
        pollutants: Pollutants = {
            "pm25": airquality_hourly_data["pm2_5"][0],
            "pm10": airquality_hourly_data["pm10"][0],
            "o3": airquality_hourly_data["ozone"][0],
            "co": airquality_hourly_data["carbon_monoxide"][0],
            "no2": airquality_hourly_data["nitrogen_dioxide"][0],
            "so2": airquality_hourly_data["sulphur_dioxide"][0]
        }

        # To calculate ppm/ppb
        gas_params: IdealGasParams = {
            "temp": weather_hourly_data["temperature_2m"][0],
            "pressure": weather_hourly_data["surface_pressure"][0]
        }

        # All pollutants api
        try:
            pollutant_aqis = calculate_pollutants_aqis(pollutants.copy(), gas_params)
        except ValueError as e:
            print(f"Error: {e}")
            print("AQI cannot be calculated.")
            return None

        aqi = max(pollutant_aqis.values())

        # The required data
        features: FeatureDict = {
            **pollutants,
            **gas_params,

            "aqi": aqi,

            "humidity": weather_hourly_data["relative_humidity_2m"][0],
            "wind_spd": weather_hourly_data["wind_speed_10m"][0],
            "dew_pt": weather_hourly_data["dew_point_2m"][0],

            "ts": datetime.fromisoformat(airquality_hourly_data["time"][0]).replace(tzinfo=UTC)
        }


        return features

    else:
        print("One of the response is not json.")

        return None
