import AQICard from "../common/AQICard.tsx";

import type {PredictionResponse} from "../prediction/PredictionCards.tsx";

type TodayPredictionCardProps = {
  data: PredictionResponse;
};

function TodayPredictionCard({
  data,
}: TodayPredictionCardProps) {
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