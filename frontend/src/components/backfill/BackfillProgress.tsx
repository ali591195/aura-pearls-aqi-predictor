import { useEffect, useRef, useState } from "react";

import type { BackfillPhase } from "../../hooks/useBackfill";

import "./BackfillProgress.css";

type BackfillProgressProps = {
  progress: number;
  phase: BackfillPhase;
  error: string | null;
};

const IDLE_MESSAGES = [
  "Ready to refresh the historical data...",
  "Your dataset is waiting for an update...",
  "Fetch the latest available observations...",
  "Keep the historical data up to date...",
];

const UP_TO_DATE_MESSAGES = [
  "Your prediction data is already up to date...",
  "The latest prediction is already available...",
  "No new backfill is needed right now...",
  "Your historical data is already refreshed...",
];

const RAW_MESSAGES = [
  "Waking the historical archive...",
  "Gathering atmospheric observations...",
  "Reconstructing the air quality timeline...",
  "Processing historical observations...",
];

const ENGINEERED_MESSAGES = [
  "Building the feature history...",
  "Transforming raw observations...",
  "Calculating historical features...",
  "Preparing the engineered dataset...",
  "Aligning temporal features...",
  "Finalizing the feature pipeline...",
];

const TRAINING_MESSAGES = [
  "Preparing the latest training data...",
  "Training the AQI prediction models...",
  "Optimizing the prediction models...",
  "Evaluating the newly trained models...",
  "Registering the updated models...",
];

function getPhaseLabel(
  phase: BackfillPhase,
): string {
  if (phase === "idle") {
    return "Press the button to fetch the latest data";
  }

  if (phase === "up-to-date") {
    return "Backfill is unavailable because the latest prediction is already updated";
  }

  if (phase === "raw") {
    return "Collecting historical data";
  }

  if (phase === "engineered") {
    return "Engineering historical features";
  }

  if (phase === "training") {
    return "Training prediction models";
  }

  if (phase === "completed") {
    return "Backfill and model training complete";
  }

  if (phase === "error") {
    return "Backfill interrupted";
  }

  return "";
}

function getMessages(
  phase: BackfillPhase,
): string[] {
  if (phase === "idle") {
    return IDLE_MESSAGES;
  }

  if (phase === "up-to-date") {
    return UP_TO_DATE_MESSAGES;
  }

  if (phase === "raw") {
    return RAW_MESSAGES;
  }

  if (phase === "engineered") {
    return ENGINEERED_MESSAGES;
  }

  if (phase === "training") {
    return TRAINING_MESSAGES;
  }

  return [];
}

function getRandomIndex(
  length: number,
  currentIndex: number,
): number {
  if (length <= 1) {
    return 0;
  }

  const availableIndexes = Array.from(
    { length },
    (_, index) => index,
  ).filter(
    (index) => index !== currentIndex,
  );

  return availableIndexes[
    Math.floor(
      Math.random() * availableIndexes.length,
    )
  ];
}

function BackfillProgress({
  progress,
  phase,
  error,
}: BackfillProgressProps) {
  const messages = getMessages(phase);

  const [messageIndex, setMessageIndex] =
    useState(() =>
      getRandomIndex(messages.length, -1),
    );

  const messageIndexRef =
    useRef(messageIndex);

  const phaseRef = useRef(phase);

  useEffect(() => {
    if (phaseRef.current === phase) {
      return;
    }

    phaseRef.current = phase;

    const nextMessages = getMessages(phase);

    const nextIndex = getRandomIndex(
      nextMessages.length,
      -1,
    );

    messageIndexRef.current = nextIndex;

    setMessageIndex(nextIndex);
  }, [phase]);

  useEffect(() => {
    if (messages.length <= 1) {
      return;
    }

    const interval = window.setInterval(() => {
      const nextIndex = getRandomIndex(
        messages.length,
        messageIndexRef.current,
      );

      messageIndexRef.current = nextIndex;

      setMessageIndex(nextIndex);
    }, 2800);

    return () => {
      window.clearInterval(interval);
    };
  }, [phase, messages.length]);

  const message =
    phase === "error"
      ? error ?? "Backfill failed."
      : messages[messageIndex];

  return (
    <div className="backfill-progress">
      <div
        className="backfill-progress-tooltip"
        key={`${phase}-${messageIndex}`}
      >
        {message}
      </div>

      <div className="backfill-progress-label">
        {getPhaseLabel(phase)}
      </div>

      <div className="backfill-progress-track">
        <div
          className="backfill-progress-fill"
          style={{
            width: `${progress}%`,
          }}
        />

        <span
          className="backfill-progress-star"
          style={{
            left: `${progress}%`,
          }}
        >
          ✦
        </span>
      </div>

      <div className="backfill-progress-percentage">
        {Math.round(progress)}%
      </div>
    </div>
  );
}

export default BackfillProgress;