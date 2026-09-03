import { useEffect, useState } from "react";

import {
  getBackendApiUrl,
  postApi,
} from "../utils/api";

export type BackfillPhase =
  | "idle"
  | "up-to-date"
  | "raw"
  | "engineered"
  | "training"
  | "completed"
  | "error";

export type BackfillResponse = {
  message: string;
  start_date: string;
  end_date: string;
};

export type ModelTrainingResponse = {
  message: string;
};

type BackfillResult = {
  raw: BackfillResponse;
  engineered: BackfillResponse;
  training: ModelTrainingResponse;
};

const RAW_BACKFILL_API_URL = getBackendApiUrl(
  "/api/backfill/raw",
);

const ENGINEERED_BACKFILL_API_URL =
  getBackendApiUrl(
    "/api/backfill/engineered",
  );

const MODEL_TRAINING_API_URL =
  getBackendApiUrl(
    "/api/model/train",
  );

async function runRawBackfill(): Promise<BackfillResponse> {
  return postApi<BackfillResponse>(
    RAW_BACKFILL_API_URL,
    "Raw backfill request failed",
  );
}

async function runEngineeredBackfill(): Promise<BackfillResponse> {
  return postApi<BackfillResponse>(
    ENGINEERED_BACKFILL_API_URL,
    "Engineered backfill request failed",
  );
}

async function runModelTraining(): Promise<ModelTrainingResponse> {
  return postApi<ModelTrainingResponse>(
    MODEL_TRAINING_API_URL,
    "Model training request failed",
  );
}

function isYesterday(timestamp: string): boolean {
  const predictionDate = new Date(timestamp);

  if (Number.isNaN(predictionDate.getTime())) {
    return false;
  }

  const yesterday = new Date();

  yesterday.setHours(0, 0, 0, 0);
  yesterday.setDate(
    yesterday.getDate() - 1,
  );

  predictionDate.setHours(0, 0, 0, 0);

  return (
    predictionDate.getTime() ===
    yesterday.getTime()
  );
}

function useBackfill(
  predictionTimestamp: string | null,
  onBackfillComplete: () => Promise<void>,
) {
  const [phase, setPhase] =
    useState<BackfillPhase>("idle");

  const [progress, setProgress] =
    useState(0);

  const [error, setError] =
    useState<string | null>(null);

  const [result, setResult] =
    useState<BackfillResult | null>(null);

  const isRunning =
    phase === "raw" ||
    phase === "engineered" ||
    phase === "training";

  useEffect(() => {
    if (!predictionTimestamp) {
      return;
    }

    if (isYesterday(predictionTimestamp)) {
      setPhase("up-to-date");
      setProgress(100);
      return;
    }

    setPhase("idle");
    setProgress(0);
  }, [predictionTimestamp]);

  useEffect(() => {
    if (!isRunning && phase !== "completed") {
      return;
    }

    const interval = window.setInterval(() => {
      setProgress((currentProgress) => {
        let increment = 0;

        if (phase === "raw") {
          increment =
            currentProgress < 25
              ? 0.12
              : 0.035;

          return Math.min(
            currentProgress + increment,
            50,
          );
        }

        if (phase === "engineered") {
          increment =
            currentProgress < 75
              ? 0.12
              : 0.025;

          return Math.min(
            currentProgress + increment,
            75,
          );
        }

        if (phase === "training") {
          increment =
            currentProgress < 95
              ? 0.035
              : 0.01;

          return Math.min(
            currentProgress + increment,
            99,
          );
        }

        if (phase === "completed") {
          increment = 1.5;

          return Math.min(
            currentProgress + increment,
            100,
          );
        }

        return currentProgress;
      });
    }, 100);

    return () => {
      window.clearInterval(interval);
    };
  }, [phase, isRunning]);

  async function startBackfill() {
    if (
      isRunning ||
      phase === "up-to-date"
    ) {
      return;
    }

    setPhase("raw");
    setProgress(0);
    setError(null);
    setResult(null);

    try {
      const rawResult =
        await runRawBackfill();

      setProgress((currentProgress) =>
        Math.max(currentProgress, 25),
      );

      setPhase("engineered");

      const engineeredResult =
        await runEngineeredBackfill();

      setProgress((currentProgress) =>
        Math.max(currentProgress, 75),
      );

      setPhase("training");

      const trainingResult =
        await runModelTraining();

      await onBackfillComplete();

      setResult({
        raw: rawResult,
        engineered: engineeredResult,
        training: trainingResult,
      });

      setPhase("completed");
      setProgress(100);
    } catch (error) {
      setPhase("error");

      setError(
        error instanceof Error
          ? error.message
          : "Backfill failed.",
      );
    }
  }

  return {
    phase,
    progress,
    error,
    result,
    isRunning,
    startBackfill,
  };
}

export default useBackfill;
