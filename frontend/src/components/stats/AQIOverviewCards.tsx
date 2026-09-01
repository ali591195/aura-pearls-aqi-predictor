import type {
  CurrentAirQualityResponse,
} from "../../hooks/useCurrentAirQuality.ts";

import "./AQIOverviewCards.css";
import {AQISymbol, getAQICategory} from "../../utils/aqi.tsx";
import {formatCurrentDateTime, formatDate} from "../../utils/date.ts";

type AQIOverviewCardsProps = {
  data: CurrentAirQualityResponse;
};

function AQIOverviewCard({
  value,
  title,
  valueLabel,
  date,
}: {
  value: number;
  title: string;
  valueLabel: string;
  date: string;
}) {
  const category = getAQICategory(value);

  return (
    <article
      className={`card aqi-overview-card ${category.className}`}
    >
      <div className="card-top">
        <span className="card-label aqi-overview-card-title">
          {title}
        </span>

        <span className="aqi-overview-card-symbol">
          <AQISymbol value={value} />
        </span>
      </div>

      <div className="aqi-overview-card-main">
        <span className="aqi-overview-card-value">
          {Math.round(value)}
        </span>

        <div className="aqi-overview-card-info">
          <span className="aqi-overview-card-value-label">
            {valueLabel}
          </span>

          <span className="aqi-overview-card-category">
            {category.label}
          </span>

          <span className="aqi-overview-card-date">
            {date}
          </span>
        </div>
      </div>
    </article>
  );
}

function AQIOverviewCards({
  data,
}: AQIOverviewCardsProps) {
  return (
    <div className="aqi-overview-cards">
      <AQIOverviewCard
        value={data.us_aqi}
        title="Current AQI"
        valueLabel="US AQI"
        date={formatCurrentDateTime(data.ts)}
      />

      <AQIOverviewCard
        value={data.today_us_aqi_mean}
        title="Today's AQI"
        valueLabel="AQI mean"
        date={formatDate(data.ts)}
      />
    </div>
  );
}

export default AQIOverviewCards;