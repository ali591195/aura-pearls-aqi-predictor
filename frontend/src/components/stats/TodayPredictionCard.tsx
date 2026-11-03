import AQICard from "../common/AQICard.tsx";

import type { PredictionResponse } from "../prediction/PredictionCards.tsx";
import NotificationCard from "./NotificationCard.tsx";
import { isPredictionFresh } from "../../utils/freshness.ts";

type TodayPredictionCardProps = {
  data: PredictionResponse;
  toggle_notice?: boolean
};

function TodayPredictionCard({
  data, toggle_notice = true
}: TodayPredictionCardProps) {
  if (toggle_notice)
    if (!isPredictionFresh(data.ts))
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
