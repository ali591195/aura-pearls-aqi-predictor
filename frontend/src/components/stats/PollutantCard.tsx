import "./PollutantCard.css";

type PollutantCardProps = {
  name: string;
  value: number;
  unit: string;
  timestamp: string;
};

function formatTime(timestamp: string): string {
  return new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Karachi",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  }).format(new Date(timestamp));
}

function PollutantCard({
  name,
  value,
  unit,
  timestamp,
}: PollutantCardProps) {
  return (
    <article className="card pollutant-card">
      <div className="pollutant-card-top">
        <span className="pollutant-card-name">
          {name}
        </span>

        <span className="pollutant-card-time">
          {formatTime(timestamp)}
        </span>
      </div>

      <div className="pollutant-card-value-row">
        <span className="pollutant-card-value">
          {Number(value).toFixed(1)}
        </span>

        <span className="pollutant-card-unit">
          {unit}
        </span>
      </div>
    </article>
  );
}

export default PollutantCard;