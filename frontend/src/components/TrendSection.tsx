import {
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";

import type { PredictionResponse } from "./PredictionCards";

import "./TrendSection.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
);

type TrendSectionProps = {
  data: PredictionResponse;
};

function TrendSection({ data }: TrendSectionProps) {
  const chartData = {
    labels: ["Day 1", "Day 2", "Day 3", "Day 4"],
    datasets: [
      {
        data: [
          data.aqi_pred_day_1,
          data.aqi_pred_day_2,
          data.aqi_pred_day_3,
          data.aqi_pred_day_4,
        ],
        borderColor: "#0891b2",
        backgroundColor: "rgba(34, 211, 238, 0.08)",
        pointBackgroundColor: "#0891b2",
        pointBorderColor: "#f8fafc",
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        borderWidth: 2,
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,

    interaction: {
      intersect: false,
      mode: "index" as const,
    },

    plugins: {
      legend: {
        display: false,
      },

      tooltip: {
        displayColors: false,

        backgroundColor: "rgba(15, 23, 42, 0.92)",
        titleColor: "#f8fafc",
        bodyColor: "#e2e8f0",

        padding: 10,

        callbacks: {
          label: (context: { parsed: { y: number | null } }) =>
            `AQI mean: ${Math.round(context.parsed.y ?? 0)}`,
        },
      },
    },

    scales: {
      x: {
        grid: {
          display: false,
        },

        border: {
          display: false,
        },

        ticks: {
          color: "rgba(15, 23, 42, 0.55)",
          font: {
            family: "Inter",
            size: 12,
          },
        },
      },

      y: {
        beginAtZero: true,

        grid: {
          color: "rgba(15, 23, 42, 0.07)",
        },

        border: {
          display: false,
        },

        ticks: {
          color: "rgba(15, 23, 42, 0.5)",
          font: {
            family: "Inter",
            size: 11,
          },
        },
      },
    },
  };

  return (
    <section className="trend-section">
      <div className="trend-section-heading">
        <div>
          <h2>4-Day AQI Trend</h2>
          <p>Predicted daily AQI mean</p>
        </div>
      </div>

      <div className="trend-chart-card">
        <div className="trend-chart">
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>
    </section>
  );
}

export default TrendSection;