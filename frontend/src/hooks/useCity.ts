import { useState } from "react";

import type { PredictionResponse } from "../components/prediction/PredictionCards.tsx";
import type { CurrentAirQualityResponse } from "./useCurrentAirQuality";
import type { CurrentWeatherResponse } from "./useCurrentWeather";

import {
    getBackendApiUrl, postApi,
} from "../utils/api";

export type CityResponse = {
  prediction: PredictionResponse;
  current_air_quality: CurrentAirQualityResponse;
  current_weather: CurrentWeatherResponse;
};

export type CityRequest = {
  latitude: number;
  longitude: number;
};

const CITY_API_URL =
  getBackendApiUrl("/api/city");

async function fetchCity(
  request: CityRequest,
): Promise<CityResponse> {
  return postApi<CityResponse>(
    CITY_API_URL,
    "City request failed",
    request,
  );
}

function useCity() {
  const [data, setData] =
    useState<CityResponse | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  async function submitCity(
    latitude: number,
    longitude: number,
  ) {
    setLoading(true);
    setError(null);

    try {
      const cityData = await fetchCity({
        latitude,
        longitude,
      });

      setData(cityData);
    } catch (error) {
      console.error(
        "Failed to fetch city data:",
        error,
      );

      setData(null);

      setError(
        error instanceof Error
          ? error.message
          : "Failed to fetch city data.",
      );
    } finally {
      setLoading(false);
    }
  }

  return {
    data,
    loading,
    error,
    submitCity,
  };
}

export default useCity;

