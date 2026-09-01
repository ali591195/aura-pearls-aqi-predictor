import AQICard from "../common/AQICard.tsx";

import "./PredictionCards.css";
import {getDay1Label, getForecastDate} from "../../utils/date.ts";
import {AQISymbol, getAQICategory} from "../../utils/aqi.tsx";

export type PredictionResponse = {
  aqi_pred_day_1: number;
  aqi_pred_day_2: number;
  aqi_pred_day_3: number;
  aqi_pred_day_4: number;
  ts: string;
};

type PredictionCardsProps = {
  data: PredictionResponse;
};

function PredictionCards({ data }: PredictionCardsProps) {
  const baseDate = new Date(data.ts);

  const predictions = [
    data.aqi_pred_day_1,
    data.aqi_pred_day_2,
    data.aqi_pred_day_3,
    data.aqi_pred_day_4,
  ];

  const [day1, ...remainingPredictions] = predictions;

  return (
    <div className="prediction-cards">
      <AQICard
        value={day1}
        label="Day 1"
        date={getDay1Label(baseDate)}
      />

      <div className="prediction-secondary-cards">
        {remainingPredictions.map((value, index) => {
          const forecastDay = index + 2;
          const category = getAQICategory(value);

          return (
            <article
              className={`card prediction-card prediction-card-secondary ${category.className}`}
              key={forecastDay}
            >
              <div className="prediction-secondary-main">
                <span className="prediction-value-secondary">
                  {Math.round(value)}
                </span>

                <div className="prediction-secondary-info">
                  <span className="card-label">
                    AQI mean
                  </span>

                  <span className="card-category">
                    {category.label}
                  </span>

                  <span className="card-date">
                    {getForecastDate(
                      baseDate,
                      forecastDay,
                    )}
                  </span>
                </div>
              </div>

              <span className="card-symbol">
                <AQISymbol value={value} />
              </span>
            </article>
          );
        })}
      </div>
    </div>
  );
}

export default PredictionCards;