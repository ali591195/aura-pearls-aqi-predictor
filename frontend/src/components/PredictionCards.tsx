import "./PredictionCards.css";

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

type AQICategory = {
  label: string;
  className: string;
};

function getAQICategory(value: number): AQICategory {
  if (value <= 50) {
    return {
      label: "Good",
      className: "aqi-good",
    };
  }

  if (value <= 100) {
    return {
      label: "Moderate",
      className: "aqi-moderate",
    };
  }

  if (value <= 150) {
    return {
      label: "Unhealthy for Sensitive Groups",
      className: "aqi-sensitive",
    };
  }

  if (value <= 200) {
    return {
      label: "Unhealthy",
      className: "aqi-unhealthy",
    };
  }

  if (value <= 300) {
    return {
      label: "Very Unhealthy",
      className: "aqi-very-unhealthy",
    };
  }

  return {
    label: "Hazardous",
    className: "aqi-hazardous",
  };
}

function formatDate(date: Date): string {
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function getForecastDate(
  baseDate: Date,
  forecastDay: number,
): string {
  const forecastDate = new Date(baseDate);

  forecastDate.setUTCDate(
    forecastDate.getUTCDate() + forecastDay
  );

  return formatDate(forecastDate);
}

function getDay1Label(baseDate: Date): string {
  const yesterday = new Date();

  yesterday.setUTCHours(0, 0, 0, 0);
  yesterday.setUTCDate(yesterday.getUTCDate() - 1);

  const base = new Date(baseDate);

  base.setUTCHours(0, 0, 0, 0);

  if (base.getTime() === yesterday.getTime()) {
    return "Today";
  }

  return getForecastDate(baseDate, 1);
}

function AQISymbol({ value }: { value: number }) {
  if (value <= 50) {
    return (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <path d="M5 13l4 4L19 7" />
      </svg>
    );
  }

  if (value <= 100) {
    return (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        aria-hidden="true"
      >
        <path d="M5 12h14" />
      </svg>
    );
  }

  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M12 3 2.8 20h18.4L12 3Z" />
      <path d="M12 9v5" />
      <circle cx="12" cy="17.2" r="0.7" fill="currentColor" />
    </svg>
  );
}

function PredictionCards({ data }: PredictionCardsProps) {
  const baseDate = new Date(data.ts);

  const predictions = [
    data.aqi_pred_day_1,
    data.aqi_pred_day_2,
    data.aqi_pred_day_3,
    data.aqi_pred_day_4,
  ];

  const [day1, ...remainingPredictions] = predictions;

  const day1Category = getAQICategory(day1);

  return (
    <div className="prediction-cards">
      <article
        className={`prediction-card prediction-card-primary ${day1Category.className}`}
      >
        <div className="prediction-card-top">
          <span className="prediction-day-label">
            Day 1
          </span>

          <span className="prediction-symbol">
            <AQISymbol value={day1} />
          </span>
        </div>

        <div className="prediction-primary-content">
          <span className="prediction-value-primary">
            {Math.round(day1)}
          </span>

          <span className="prediction-aqi-label">
            AQI mean
          </span>

          <span className="prediction-category">
            {day1Category.label}
          </span>

          <span className="prediction-date prediction-date-primary">
            {getDay1Label(baseDate)}
          </span>
        </div>
      </article>

      <div className="prediction-secondary-cards">
        {remainingPredictions.map((value, index) => {
          const forecastDay = index + 2;
          const category = getAQICategory(value);

          return (
            <article
              className={`prediction-card prediction-card-secondary ${category.className}`}
              key={forecastDay}
            >
              <div className="prediction-secondary-main">
                <span className="prediction-value-secondary">
                  {Math.round(value)}
                </span>

                <div className="prediction-secondary-info">
                  <span className="prediction-aqi-label">
                    AQI mean
                  </span>

                  <span className="prediction-category">
                    {category.label}
                  </span>

                  <span className="prediction-date">
                    {getForecastDate(
                      baseDate,
                      forecastDay,
                    )}
                  </span>
                </div>
              </div>

              <span className="prediction-symbol">
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