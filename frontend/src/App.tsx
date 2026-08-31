import { useEffect, useState } from "react";

import Aurora from "./components/Aurora";
import Footer from "./components/Footer";
import PageHeader from "./components/PageHeader";
import PredictionCards from "./components/PredictionCards";
import PredictionSection from "./components/PredictionSection";
import Sidebar from "./components/Sidebar";
import TrendSection from "./components/TrendSection";

import type { PredictionResponse } from "./components/PredictionCards";

import "./App.css";

const backendHost = import.meta.env.VITE_BACKEND_HOST;
const backendPort = import.meta.env.VITE_BACKEND_PORT;

const PREDICTION_API_URL = backendPort
  ? `http://${backendHost}:${backendPort}/api/prediction`
  : `https://${backendHost}/api/prediction`;

const PREDICTION_CACHE_KEY = "aura_prediction_cache";

type CachedPrediction = {
  cachedDate: string;
  data: PredictionResponse;
};

function getTodayKey(): string {
  return new Date().toISOString().slice(0, 10);
}

function getCachedPrediction(): PredictionResponse | null {
  const cached = localStorage.getItem(
    PREDICTION_CACHE_KEY,
  );

  if (!cached) {
    return null;
  }

  try {
    const parsed: CachedPrediction = JSON.parse(cached);

    if (parsed.cachedDate !== getTodayKey()) {
      localStorage.removeItem(PREDICTION_CACHE_KEY);
      return null;
    }

    return parsed.data;
  } catch {
    localStorage.removeItem(PREDICTION_CACHE_KEY);
    return null;
  }
}

function savePredictionCache(data: PredictionResponse): void {
  const cached: CachedPrediction = {
    cachedDate: getTodayKey(),
    data,
  };

  localStorage.setItem(
    PREDICTION_CACHE_KEY,
    JSON.stringify(cached),
  );
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
  const response = await fetch(PREDICTION_API_URL);

  if (!response.ok) {
    throw new Error(
      `Prediction request failed: ${response.status}`,
    );
  }

  return response.json();
}

function App() {
  const [prediction, setPrediction] =
    useState<PredictionResponse | null>(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const cachedPrediction = getCachedPrediction();

    if (cachedPrediction) {
      setPrediction(cachedPrediction);
      setLoading(false);
      return;
    }

    void refreshPrediction();
  }, []);

  async function refreshPrediction() {
    setLoading(true);

    try {
      const newPrediction = await fetchPrediction();

      const cachedPrediction = getCachedPrediction();

      if (
        isPredictionDifferent(
          cachedPrediction,
          newPrediction,
        )
      ) {
        savePredictionCache(newPrediction);
      }

      setPrediction(newPrediction);
    } catch (error) {
      console.error("Failed to fetch prediction:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <Aurora />

      <div className="app-layout">
        <Sidebar />

        <section className="main-content">
          <PageHeader
            title="Prediction"
            subtitle="Lahore"
          />

          <PredictionSection
            onRefresh={refreshPrediction}
            loading={loading}
          />

          {prediction && (
              <>
                <PredictionCards data={prediction} />
                <TrendSection data={prediction} />
              </>
          )}
        </section>
      </div>

      <Footer />
    </main>
  );
}

export default App;