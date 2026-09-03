import { Link } from "react-router-dom";
import "./DataFreshnessNotice.css";

type DataFreshnessNoticeProps = {
  date: string | Date;
};

function DataFreshnessNotice({
  date,
}: DataFreshnessNoticeProps) {
  const predictionDate = new Date(date);

  if (Number.isNaN(predictionDate.getTime())) {
    return null;
  }

  const yesterday = new Date();
  yesterday.setHours(0, 0, 0, 0);
  yesterday.setDate(yesterday.getDate() - 1);

  predictionDate.setHours(0, 0, 0, 0);

  const isOld = predictionDate < yesterday;

  if (!isOld) {
    return null;
  }

  const latestPredictionDate = new Date(predictionDate);
  latestPredictionDate.setDate(
    latestPredictionDate.getDate() + 1,
  );

  return (
    <section className="data-freshness-notice">
      <div className="data-freshness-notice-content">
        <div className="data-freshness-notice-text">
          <h2>Prediction data is outdated</h2>

          <p>
            The latest available prediction is for{" "}
            <strong>
              {latestPredictionDate.toLocaleDateString("en-US", {
                month: "short",
                day: "numeric",
                year: "numeric",
              })}
            </strong>
            . Run a manual backfill to fetch the latest available data.
          </p>
        </div>

        <Link
          to="/backfill"
          className="data-freshness-notice-action"
        >
          Go to Backfill
        </Link>
      </div>
    </section>
  );
}

export default DataFreshnessNotice;