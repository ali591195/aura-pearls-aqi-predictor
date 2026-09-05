import "./PredictionLoadingSkeleton.css";

function PredictionLoadingSkeleton() {
  return (
    <div
      className="prediction-loading-skeleton"
      aria-label="Loading prediction data"
    >
      <div className="prediction-skeleton-refresh">
        <span className="prediction-skeleton-refresh-title" />

        <span className="prediction-skeleton-refresh-button" />
      </div>

      <div className="prediction-skeleton-freshness">
        <div className="prediction-skeleton-freshness-lines">
          <span className="prediction-skeleton-line prediction-skeleton-line-title" />
          <span className="prediction-skeleton-line prediction-skeleton-line-text" />
        </div>

        <span className="prediction-skeleton-freshness-button" />
      </div>

      <div className="prediction-skeleton-cards">
        <span className="prediction-skeleton-card" />
        <span className="prediction-skeleton-card" />
        <span className="prediction-skeleton-card" />
        <span className="prediction-skeleton-card" />
      </div>
    </div>
  );
}

export default PredictionLoadingSkeleton;