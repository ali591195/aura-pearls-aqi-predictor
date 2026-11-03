import { Link } from "react-router-dom";
import "./DataFreshnessNotice.css";
import {
  getPredictionTargetDate,
  isPredictionFresh,
} from "../../utils/freshness.ts";

type DataFreshnessNoticeProps = {
  date: string | Date;
};

function DataFreshnessNotice({
  date,
}: DataFreshnessNoticeProps) {
  const latestPredictionDate = getPredictionTargetDate(date);

  if (latestPredictionDate === null || isPredictionFresh(date)) {
    return null;
  }

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