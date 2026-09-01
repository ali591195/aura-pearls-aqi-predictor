import type { ReactNode } from "react";

import SectionHeader from "../common/SectionHeader.tsx";

import "./WeatherSection.css";

type WeatherSectionProps = {
  children?: ReactNode;
};

function WeatherSection({
  children,
}: WeatherSectionProps) {
  return (
    <section className="weather-section">
      <SectionHeader
        title="Weather"
        subtitle="Current weather conditions in Lahore"
      />

      <div className="weather-content">
        {children}
      </div>
    </section>
  );
}

export default WeatherSection;