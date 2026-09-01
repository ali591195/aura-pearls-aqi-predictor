import { useEffect, useState } from "react";

import type { PredictionResponse } from "../components/prediction/PredictionCards.tsx";
import {
  getBackendApiUrl,
  fetchApi,
} from "../utils/api";
import {
  readCache,
  readValidCache,
  saveCache,
} from "../utils/cache";

const PREDICTION_API_URL =
  getBackendApiUrl("/api/prediction");

const PREDICTION_CACHE_KEY =
  "aura_prediction_cache";

function getTodayExpiration(): Date {
  const tomorrow = new Date();

  tomorrow.setUTCDate(
    tomorrow.getUTCDate() + 1,
  );

  tomorrow.setUTCHours(0, 0, 0, 0);

  return tomorrow;
}

function isPredictionDifferent(
  oldData: PredictionResponse | null,
  newData: PredictionResponse,
): boolean {
  if (!oldData) {
    return true;
  }

  return (
    oldData.aqi_pred_day_1 !== newData.aqi_pred_day_1 ||
    oldData.aqi_pred_day_2 !== newData.aqi_pred_day_2 ||
    oldData.aqi_pred_day_3 !== newData.aqi_pred_day_3 ||
    oldData.aqi_pred_day_4 !== newData.aqi_pred_day_4 ||
    oldData.ts !== newData.ts
  );
}

async function fetchPrediction(): Promise<PredictionResponse> {
  return fetchApi<PredictionResponse>(
    PREDICTION_API_URL,
    "Prediction request failed",
  );
}

function usePrediction() {
  const [prediction, setPrediction] =
    useState<PredictionResponse | null>(null);

  const [loading, setLoading] = useState(true);

  async function refreshPrediction() {
    setLoading(true);

    try {
      const newPrediction =
        await fetchPrediction();

      const cached = readCache<PredictionResponse>(
        PREDICTION_CACHE_KEY,
      );

      const oldPrediction =
        cached?.data ?? null;

      if (
        isPredictionDifferent(
          oldPrediction,
          newPrediction,
        )
      ) {
        saveCache(
          PREDICTION_CACHE_KEY,
          newPrediction,
          getTodayExpiration(),
        );
      }

      setPrediction(newPrediction);
    } catch (error) {
      console.error(
        "Failed to fetch prediction:",
        error,
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const cachedPrediction =
      readValidCache<PredictionResponse>(
        PREDICTION_CACHE_KEY,
      );

    if (cachedPrediction) {
      setPrediction(cachedPrediction);
      setLoading(false);
      return;
    }

    void refreshPrediction();
  }, []);

  return {
    prediction,
    loading,
    refreshPrediction,
  };
}

export default usePrediction;