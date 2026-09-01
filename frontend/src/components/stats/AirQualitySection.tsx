import type { ReactNode } from "react";
import SectionHeader from "../common/SectionHeader.tsx";

import "./AirQualitySection.css";

type AirQualitySectionProps = {
  children?: ReactNode;
};

function AirQualitySection({
  children,
}: AirQualitySectionProps) {
  return (
    <section className="air-quality-section">
      <SectionHeader
        title="Air Quality"
        subtitle="Current air quality conditions in Lahore"
      />

      <div className="air-quality-content">
        {children}
      </div>
    </section>
  );
}

export default AirQualitySection;