import "./CityLoadingSkeleton.css";

function CityLoadingSkeleton() {
  return (
    <div
      className="city-loading-skeleton"
      aria-label="Loading city data"
    >
      <div className="city-skeleton-freshness">
        <div className="city-skeleton-lines">
          <span
            className="
              city-skeleton-line
              city-skeleton-line-title
            "
          />

          <span
            className="
              city-skeleton-line
              city-skeleton-line-text
            "
          />
        </div>

        <span className="city-skeleton-button" />
      </div>

      <div className="city-skeleton-prediction-grid">
        <span className="city-skeleton-card" />
        <span className="city-skeleton-card" />
        <span className="city-skeleton-card" />
        <span className="city-skeleton-card" />
      </div>

      <div className="city-skeleton-section">
        <span className="city-skeleton-section-title" />

        <div className="city-skeleton-aqi-grid">
          <span className="city-skeleton-large-card" />
          <span className="city-skeleton-large-card" />
        </div>

        <div className="city-skeleton-pollutant-grid">
          <span className="city-skeleton-small-card" />
          <span className="city-skeleton-small-card" />
          <span className="city-skeleton-small-card" />
        </div>

        <div className="city-skeleton-pollutant-grid">
          <span className="city-skeleton-small-card" />
          <span className="city-skeleton-small-card" />
          <span className="city-skeleton-small-card" />
        </div>
      </div>

      <div className="city-skeleton-section">
        <span className="city-skeleton-section-title" />

        <div className="city-skeleton-aqi-grid">
          <span className="city-skeleton-large-card" />
          <span className="city-skeleton-large-card" />
        </div>

        <div className="city-skeleton-pollutant-grid">
          <span className="city-skeleton-small-card" />
          <span className="city-skeleton-small-card" />
          <span className="city-skeleton-small-card" />
        </div>
      </div>
    </div>
  );
}

export default CityLoadingSkeleton;

