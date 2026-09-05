import "./CityModelNotice.css";

function CityModelNotice() {
  return (
    <section className="city-model-notice">
      <div className="city-model-notice-content">
        <div className="city-model-notice-text">
          <h2>City predictions may vary in accuracy</h2>

          <p>
            This model was trained exclusively on historical data from{" "}
            <strong>Lahore</strong>. Predictions for other cities may have
            lower and more variable accuracy due to differences in local
            environmental and air-quality patterns.
          </p>
        </div>
      </div>
    </section>
  );
}

export default CityModelNotice;