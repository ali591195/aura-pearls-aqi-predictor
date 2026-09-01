import "./AQICard.css";
import {AQISymbol, getAQICategory} from "../../utils/aqi.tsx";

type AQICardProps = {
  value: number;
  label: string;
  valueLabel?: string;
  category?: string;
  date?: string;
  symbol?: boolean;
};

function AQICard({
  value,
  label,
  valueLabel = "AQI mean",
  category,
  date,
  symbol = true,
}: AQICardProps) {
  const aqiCategory = getAQICategory(value);

  return (
    <article
      className={`card aqi-card ${aqiCategory.className}`}
    >
      <div className="card-top">
        <span className="card-label">{label}</span>

        {symbol && (
          <span className="card-symbol">
            <AQISymbol value={value} />
          </span>
        )}
      </div>

      <div className="aqi-card-content">
        <span className="aqi-card-value">
          {Math.round(value)}
        </span>

        <span className="card-label">
          {valueLabel}
        </span>

        <span className="card-category">
          {category ?? aqiCategory.label}
        </span>

        {date && (
          <span className="card-date aqi-card-date">
            {date}
          </span>
        )}
      </div>
    </article>
  );
}

export default AQICard;