import { useEffect, useState } from "react";

import {
  fetchApi,
  getBackendApiUrl,
} from "../utils/api";

import {
  readValidCache,
  saveCache,
} from "../utils/cache";

export type CurrentWeatherResponse = {
  ts: string;

  temperature: number;
  humidity: number;
  pressure: number;
  wind_speed: number;
  dew_point: number;

  unit_temperature: string;
  unit_humidity: string;
  unit_pressure: string;
  unit_wind_speed: string;
  unit_dew_point: string;
};

const CURRENT_WEATHER_API_URL =
  getBackendApiUrl("/api/current-weather");

const CURRENT_WEATHER_CACHE_KEY =
  "aura_current_weather_cache";

function getNextHourExpiration(): Date {
  const nextHour = new Date();

  nextHour.setMinutes(0, 0, 0);
  nextHour.setHours(nextHour.getHours() + 1);

  return nextHour;
}

async function fetchCurrentWeather(): Promise<CurrentWeatherResponse> {
  return fetchApi<CurrentWeatherResponse>(
    CURRENT_WEATHER_API_URL,
    "Current weather request failed",
  );
}

function useCurrentWeather() {
  const [data, setData] =
    useState<CurrentWeatherResponse | null>(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    const cachedData =
      readValidCache<CurrentWeatherResponse>(
        CURRENT_WEATHER_CACHE_KEY,
      );

    if (cachedData) {
      setData(cachedData);
      setLoading(false);
      return;
    }

    void (async () => {
      try {
        const freshData =
          await fetchCurrentWeather();

        saveCache(
          CURRENT_WEATHER_CACHE_KEY,
          freshData,
          getNextHourExpiration(),
        );

        setData(freshData);
      } catch (error) {
        console.error(
          "Failed to fetch current weather:",
          error,
        );

        setError(
          error instanceof Error
            ? error.message
            : "Failed to fetch current weather.",
        );
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return {
    data,
    loading,
    error,
  };
}

export default useCurrentWeather;