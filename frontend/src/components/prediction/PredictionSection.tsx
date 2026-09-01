import SectionHeader from "../common/SectionHeader.tsx";
import "./PredictionSection.css";

type PredictionSectionProps = {
  onRefresh: () => void;
  loading: boolean;
};

function RefreshIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M20 11a8.1 8.1 0 0 0-14-4.9L4 8" />
      <path d="M4 4v4h4" />
      <path d="M4 13a8.1 8.1 0 0 0 14 4.9l2-1.9" />
      <path d="M20 20v-4h-4" />
    </svg>
  );
}

function PredictionSection({
  onRefresh,
  loading,
}: PredictionSectionProps) {
  return (
    <section className="prediction-section">
      <SectionHeader
        title="Air Quality Forecast"
        subtitle="Predicted AQI for the upcoming days"
        action={
          <button
            className={`prediction-refresh ${
              loading ? "loading" : ""
            }`}
            type="button"
            onClick={onRefresh}
            disabled={loading}
            aria-label="Refresh prediction"
            title="Refresh prediction"
          >
            <RefreshIcon />
          </button>
        }
      />
    </section>
  );
}

export default PredictionSection;