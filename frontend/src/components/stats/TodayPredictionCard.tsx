import AQICard from "../common/AQICard.tsx";

import type { PredictionResponse } from "../prediction/PredictionCards.tsx";
import NotificationCard from "./NotificationCard.tsx";

type TodayPredictionCardProps = {
  data: PredictionResponse;
  toggle_notice?: boolean
};

function isToday(timestamp: string): boolean {
  const predictionDate = new Date(timestamp);

  if (Number.isNaN(predictionDate.getTime())) {
    return false;
  }

  predictionDate.setDate(
    predictionDate.getDate() + 1,
  );

  const today = new Date();

  return (
    predictionDate.getFullYear() === today.getFullYear() &&
    predictionDate.getMonth() === today.getMonth() &&
    predictionDate.getDate() === today.getDate()
  );
}

function TodayPredictionCard({
  data, toggle_notice = true
}: TodayPredictionCardProps) {
  if (toggle_notice)
    if (!isToday(data.ts))
      return <NotificationCard />;

  return (
    <AQICard
      value={data.aqi_pred_day_1}
      label="Today's Prediction"
      valueLabel="AQI mean"
      date="Today"
    />
  );
}

export default TodayPredictionCard;