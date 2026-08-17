from math import floor

from src.archived.epa_aqi.aqi_constants import POLLUTANTS_MAX_CONCENTRATION, POLLUTANTS_BREAKPOINTS, \
    POLLUTANTS_CONVERSION_DATA, UNIVERSAL_GAS_CONSTANT
from src.archived.epa_aqi.aqi_schemas import Pollutants, IdealGasParams


def calculate_pollutants_aqis(pollutants: Pollutants, ideal_gas_law_params: IdealGasParams) -> Pollutants:
    """
        Convert each pollutant into its respective aqi

        :param pollutants: Pollutant values
        :param ideal_gas_law_params: Contain temperature and pressure
        :return: A dictionary of pollutants aqi
        :raises ValueError: When value is invalid
    """

    convert_to_epa_units(temp_c=ideal_gas_law_params["temp"], pressure_hpa= ideal_gas_law_params["pressure"], pollutants=pollutants)

    # Formatting for EQA
    format_pollutants(pollutants)

    aqis: Pollutants = {}

    for pollutant, concentration in pollutants.items():
        if concentration < 0:
            raise ValueError(f"{pollutant.capitalize()} cannot be negative.")

        if concentration > POLLUTANTS_MAX_CONCENTRATION[pollutant]:
            aqis[pollutant] = 500
        else:

            # Apply formula
            for c_low, c_high, i_low, i_high in POLLUTANTS_BREAKPOINTS[pollutant]:
                if c_low <= concentration <= c_high:
                    aqi = (
                            (i_high - i_low)
                            / (c_high - c_low)
                            * (concentration - c_low)
                            + i_low
                    )
                    aqis[pollutant] = round(aqi)
                    break

            if pollutant not in aqis:
                raise ValueError(f"Invalid {pollutant} concentration.")

    return aqis


def format_pollutants(pollutants: Pollutants) -> None:
    """
        Format pollutants according to EPA

        :param pollutants: Pollutant values
        :return: None
    """

    pollutants["pm10"] = floor(pollutants["pm10"])
    pollutants["pm25"] = floor(pollutants["pm25"] * 10) / 10

    pollutants["o3"] = floor(pollutants["o3"] * 1000) / 1000
    pollutants["co"] = floor(pollutants["co"] * 10) / 10

    pollutants["no2"] = floor(pollutants["no2"])
    pollutants["so2"] = floor(pollutants["so2"])


def convert_to_epa_units(temp_c: float, pressure_hpa: float, pollutants: Pollutants) -> None:
    """
        Convert pollutants to EPA units

        :param temp_c: Temperature in Celsius
        :param pressure_hpa: Pressure
        :param pollutants: Pollutant values
        :return: None
    """

    temp_k = temp_c + 273.15
    pressure_pa = pressure_hpa * 100

    for pollutant, (molecular_weight, unit) in POLLUTANTS_CONVERSION_DATA.items():
        pollutants[pollutant] = (pollutants[pollutant] * UNIVERSAL_GAS_CONSTANT * temp_k) / (pressure_pa * molecular_weight)

        if unit == "ppb":
            pollutants[pollutant] *= 1000