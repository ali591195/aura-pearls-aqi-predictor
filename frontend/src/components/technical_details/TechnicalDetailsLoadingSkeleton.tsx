import "./TechnicalDetailsLoadingSkeleton.css";

function TechnicalDetailsLoadingSkeleton() {
  return (
    <div
      className="technical-details-loading-skeleton"
      aria-label="Loading technical details"
    >
      <div className="technical-details-skeleton-freshness">
        <div className="technical-details-skeleton-lines">
          <span className="technical-details-skeleton-line technical-details-skeleton-line-title" />
          <span className="technical-details-skeleton-line technical-details-skeleton-line-text" />
        </div>

        <span className="technical-details-skeleton-button" />
      </div>

      <div className="technical-details-skeleton-sections">
        <div className="technical-details-skeleton-section">
          <span className="technical-details-skeleton-section-title" />
          <span className="technical-details-skeleton-section-card" />
        </div>

        <div className="technical-details-skeleton-section">
          <span className="technical-details-skeleton-section-title" />
          <span className="technical-details-skeleton-section-card" />
        </div>

        <div className="technical-details-skeleton-section">
          <span className="technical-details-skeleton-section-title" />
          <span className="technical-details-skeleton-section-card" />
        </div>

        <div className="technical-details-skeleton-section">
          <span className="technical-details-skeleton-section-title" />
          <span className="technical-details-skeleton-section-card" />
        </div>
      </div>
    </div>
  );
}

export default TechnicalDetailsLoadingSkeleton;