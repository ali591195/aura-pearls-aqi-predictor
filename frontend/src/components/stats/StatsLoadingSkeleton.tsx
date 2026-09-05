import "./StatsLoadingSkeleton.css";

export function AirQualityLoadingSkeleton() {
  return (
    <div className="stats-skeleton-content">
      <div className="stats-skeleton-aqi-grid">
        <span className="stats-skeleton-large-card" />
        <span className="stats-skeleton-large-card" />
      </div>

      <div className="stats-skeleton-pollutant-grid">
        <span className="stats-skeleton-small-card" />
        <span className="stats-skeleton-small-card" />
        <span className="stats-skeleton-small-card" />
      </div>

      <div className="stats-skeleton-pollutant-grid">
        <span className="stats-skeleton-small-card" />
        <span className="stats-skeleton-small-card" />
        <span className="stats-skeleton-small-card" />
      </div>
    </div>
  );
}

export function WeatherLoadingSkeleton() {
  return (
    <div className="stats-skeleton-content">
      <div className="stats-skeleton-aqi-grid">
        <span className="stats-skeleton-large-card" />
        <span className="stats-skeleton-large-card" />
      </div>

      <div className="stats-skeleton-pollutant-grid">
        <span className="stats-skeleton-small-card" />
        <span className="stats-skeleton-small-card" />
        <span className="stats-skeleton-small-card" />
      </div>
    </div>
  );
}