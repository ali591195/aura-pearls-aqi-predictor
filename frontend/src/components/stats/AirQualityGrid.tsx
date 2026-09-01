import type { ReactNode } from "react";

import "./AirQualityGrid.css";

type AirQualityGridProps = {
  children: ReactNode;
};

function AirQualityGrid({
  children,
}: AirQualityGridProps) {
  return (
    <div className="air-quality-grid">
      {children}
    </div>
  );
}

export default AirQualityGrid;