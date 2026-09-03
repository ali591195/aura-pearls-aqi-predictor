import { Link } from "react-router-dom";
import "./NotificationCard.css";

function NotificationCard() {
  return (
    <article className="card notification-card">
      <div className="notification-card-content">
        <h2>
          Today's prediction is not{" "}
          <span>available</span>
        </h2>

        <p>
          The latest prediction data is outdated. Run a
          manual backfill to fetch today's prediction.
        </p>

        <Link
          to="/backfill"
          className="notification-card-action"
        >
          Go to Backfill
        </Link>
      </div>
    </article>
  );
}

export default NotificationCard;