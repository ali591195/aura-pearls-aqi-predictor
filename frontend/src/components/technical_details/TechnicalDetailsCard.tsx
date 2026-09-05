import "./TechnicalDetailsCard.css";

type SHAPFeature = {
  feature: string;
  value: number;
  shap_value: number;
};

type ModelMetrics = {
  rmse: number;
  mae: number;
  r2: number;
};

type ModelTechnicalDetails = {
  model_name: string;
  model_type: string;
  target: string;
  version: number;
  metrics: ModelMetrics;
  shap: SHAPFeature[];
};

type TechnicalDetailsCardProps = {
  day: number;
  model: ModelTechnicalDetails;
};

function formatFeatureName(feature: string): string {
  return feature
    .replace(/_/g, " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase(),
    );
}

function TechnicalDetailsCard({
  day,
  model,
}: TechnicalDetailsCardProps) {
  const shapFeatures = [...model.shap].sort(
    (a, b) =>
      Math.abs(b.shap_value) -
      Math.abs(a.shap_value),
  );

  const maxShapValue =
    Math.max(
      ...shapFeatures.map((item) =>
        Math.abs(item.shap_value),
      ),
      1,
    );

  return (
    <div className="technical-details-card">
      <div className="technical-details-row technical-details-model-row">
        <article className="card technical-details-info-card">
          <span className="technical-details-card-label">
            Model Type
          </span>

          <span className="technical-details-card-value">
            {model.model_type}
          </span>
        </article>

        <article className="card technical-details-info-card">
          <span className="technical-details-card-label">
            Version
          </span>

          <span className="technical-details-card-value">
            v{model.version}
          </span>
        </article>

        <article className="card technical-details-info-card">
          <span className="technical-details-card-label">
            Forecast Day
          </span>

          <span className="technical-details-card-value">
            Day {day}
          </span>
        </article>
      </div>

      <div className="technical-details-row technical-details-metrics-row">
        <article className="card technical-details-metric-card">
          <span className="technical-details-card-label">
            RMSE
          </span>

          <span className="technical-details-metric-value">
            {model.metrics.rmse.toFixed(2)}
          </span>
        </article>

        <article className="card technical-details-metric-card">
          <span className="technical-details-card-label">
            MAE
          </span>

          <span className="technical-details-metric-value">
            {model.metrics.mae.toFixed(2)}
          </span>
        </article>

        <article className="card technical-details-metric-card">
          <span className="technical-details-card-label">
            R²
          </span>

          <span className="technical-details-metric-value">
            {model.metrics.r2.toFixed(3)}
          </span>
        </article>
      </div>

      <article className="card technical-details-shap-card">
        <div className="technical-details-shap-header">
          <div>
            <span className="technical-details-card-label">
              Local Explainability
            </span>

            <h3>SHAP Feature Contributions</h3>

            <p>
              How each feature influences the current
              prediction.
            </p>
          </div>
        </div>

        <div className="technical-details-shap-chart">
          {shapFeatures.map((item) => {
            const magnitude =
              (Math.abs(item.shap_value) /
                maxShapValue) *
              100;

            const isPositive =
              item.shap_value >= 0;

            return (
              <div
                className="technical-details-shap-row"
                key={item.feature}
              >
                <div className="technical-details-shap-feature">
                  <span>
                    {formatFeatureName(
                      item.feature,
                    )}
                  </span>

                  <span className="technical-details-shap-input">
                    {item.value.toFixed(2)}
                  </span>
                </div>

                <div className="technical-details-shap-bar-area">
                  <div
                    className={`technical-details-shap-bar ${
                      isPositive
                        ? "positive"
                        : "negative"
                    }`}
                    style={{
                      width: `${magnitude}%`,
                    }}
                  />
                </div>

                <span
                  className={`technical-details-shap-value ${
                    isPositive
                      ? "positive"
                      : "negative"
                  }`}
                >
                  {isPositive ? "+" : ""}
                  {item.shap_value.toFixed(2)}
                </span>
              </div>
            );
          })}
        </div>
      </article>
    </div>
  );
}

export default TechnicalDetailsCard;