import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  getBackendApiUrl,
  fetchApi,
} from "../utils/api";
import {
  readCache,
  readValidCache,
  saveCache,
} from "../utils/cache";

export type SHAPFeature = {
  feature: string;
  value: number;
  shap_value: number;
};

export type ModelMetrics = {
  rmse: number;
  mae: number;
  r2: number;
};

export type ModelTechnicalDetails = {
  model_name: string;
  model_type: string;
  target: string;
  version: number;
  metrics: ModelMetrics;
  shap: SHAPFeature[];
};

export type TechnicalDetailsResponse = {
  models: ModelTechnicalDetails[];
};

const TECHNICAL_DETAILS_API_URL =
  getBackendApiUrl("/api/technical-details");

const TECHNICAL_DETAILS_CACHE_KEY =
  "aura_technical_details_cache";

function getTodayExpiration(): Date {
  const tomorrow = new Date();

  tomorrow.setUTCDate(
    tomorrow.getUTCDate() + 1,
  );

  tomorrow.setUTCHours(0, 0, 0, 0);

  return tomorrow;
}

async function fetchTechnicalDetails(): Promise<TechnicalDetailsResponse> {
  return fetchApi<TechnicalDetailsResponse>(
    TECHNICAL_DETAILS_API_URL,
    "Technical details request failed",
  );
}

function useTechnicalDetails(
  predictionTimestamp?: string,
) {
  const [technicalDetails, setTechnicalDetails] =
    useState<TechnicalDetailsResponse | null>(null);

  const [loading, setLoading] = useState(true);

  const previousPredictionTimestamp =
    useRef<string | undefined>(undefined);

  useEffect(() => {
    async function loadTechnicalDetails() {
      const isPredictionRefresh =
        previousPredictionTimestamp.current !==
          undefined &&
        previousPredictionTimestamp.current !==
          predictionTimestamp;

      previousPredictionTimestamp.current =
        predictionTimestamp;

      /*
       * On the initial load, use the valid cache.
       */
      if (!isPredictionRefresh) {
        const cachedTechnicalDetails =
          readValidCache<TechnicalDetailsResponse>(
            TECHNICAL_DETAILS_CACHE_KEY,
          );

        if (cachedTechnicalDetails) {
          setTechnicalDetails(
            cachedTechnicalDetails,
          );
          setLoading(false);
          return;
        }
      }

      /*
       * Fetch when:
       * - There is no valid cache.
       * - Prediction data has refreshed.
       */
      setLoading(true);

      try {
        const newTechnicalDetails =
          await fetchTechnicalDetails();

        const cached =
          readCache<TechnicalDetailsResponse>(
            TECHNICAL_DETAILS_CACHE_KEY,
          );

        const oldTechnicalDetails =
          cached?.data ?? null;

        if (
          JSON.stringify(oldTechnicalDetails) !==
          JSON.stringify(newTechnicalDetails)
        ) {
          saveCache(
            TECHNICAL_DETAILS_CACHE_KEY,
            newTechnicalDetails,
            getTodayExpiration(),
          );
        }

        setTechnicalDetails(
          newTechnicalDetails,
        );
      } catch (error) {
        console.error(
          "Failed to fetch technical details:",
          error,
        );
      } finally {
        setLoading(false);
      }
    }

    void loadTechnicalDetails();
  }, [predictionTimestamp]);

  return {
    technicalDetails,
    loading,
  };
}

export default useTechnicalDetails;