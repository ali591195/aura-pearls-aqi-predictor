import type { CurrentWeatherResponse } from "../../hooks/useCurrentWeather.ts";

import "./WeatherOverviewCards.css";

type WeatherOverviewCardsProps = {
  data: CurrentWeatherResponse;
};

function formatCurrentTime(ts: string): string {
  return new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Karachi",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  }).format(new Date(ts));
}

function WeatherOverviewCard({
  title,
  value,
  unit,
  timestamp,
}: {
  title: string;
  value: number;
  unit: string;
  timestamp: string;
}) {
  return (
    <article className="card weather-overview-card">
      <div className="card-top">
        <span className="card-label">
          {title}
        </span>

        <span className="weather-overview-card-time">
          {formatCurrentTime(timestamp)}
        </span>
      </div>

      <div className="weather-overview-card-main">
        <span className="weather-overview-card-value">
          {Math.round(value)}
        </span>

        <div className="weather-overview-card-info">
          <span className="weather-overview-card-unit">
            {unit}
          </span>
        </div>
      </div>
    </article>
  );
}

function WeatherOverviewCards({
  data,
}: WeatherOverviewCardsProps) {
  return (
    <div className="weather-overview-cards">
      <WeatherOverviewCard
        title="Temperature"
        value={data.temperature}
        unit={data.unit_temperature}
        timestamp={data.ts}
      />

      <WeatherOverviewCard
        title="Humidity"
        value={data.humidity}
        unit={data.unit_humidity}
        timestamp={data.ts}
      />
    </div>
  );
}

export default WeatherOverviewCards;