import { useEffect, useState } from "react";

import {
  fetchApi,
  getBackendApiUrl,
} from "../utils/api";

import {
  readValidCache,
  saveCache,
} from "../utils/cache";

export type CurrentAirQualityResponse = {
  ts: string;

  us_aqi: number;
  today_us_aqi_mean: number;


  pm10: number;
  pm2_5: number;
  carbon_monoxide: number;
  nitrogen_dioxide: number;
  sulphur_dioxide: number;
  ozone: number;

  unit_pm10: string;
  unit_pm2_5: string;
  unit_carbon_monoxide: string;
  unit_nitrogen_dioxide: string;
  unit_sulphur_dioxide: string;
  unit_ozone: string;
};

const CURRENT_AIR_QUALITY_API_URL =
  getBackendApiUrl(
    "/api/current-air-quality",
  );

const CURRENT_AIR_QUALITY_CACHE_KEY =
  "aura_current_air_quality_cache";

function getNextHourExpiration(): Date {
  const nextHour = new Date();

  nextHour.setMinutes(0, 0, 0);
  nextHour.setHours(nextHour.getHours() + 1);

  return nextHour;
}

async function fetchCurrentAirQuality():
  Promise<CurrentAirQualityResponse> {
  return fetchApi<CurrentAirQualityResponse>(
    CURRENT_AIR_QUALITY_API_URL,
    "Current air quality request failed",
  );
}

function useCurrentAirQuality() {
  const [data, setData] =
    useState<CurrentAirQualityResponse | null>(
      null,
    );

  const [loading, setLoading] = useState(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    const cachedData =
      readValidCache<CurrentAirQualityResponse>(
        CURRENT_AIR_QUALITY_CACHE_KEY,
      );

    if (cachedData) {
      setData(cachedData);
      setLoading(false);
      return;
    }

    void (async () => {
      try {
        const freshData =
          await fetchCurrentAirQuality();

        saveCache(
          CURRENT_AIR_QUALITY_CACHE_KEY,
          freshData,
          getNextHourExpiration(),
        );

        setData(freshData);
      } catch (error) {
        console.error(
          "Failed to fetch current air quality:",
          error,
        );

        setError(
          error instanceof Error
            ? error.message
            : "Failed to fetch current air quality.",
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

export default useCurrentAirQuality;