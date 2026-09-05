import { useState, type ReactNode } from "react";

import "./TechnicalDetailsSection.css";

type TechnicalDetailsSectionProps = {
  day: number;
  children?: ReactNode;
  defaultOpen?: boolean;
};

function TechnicalDetailsSection({
  day,
  children,
  defaultOpen = false,
}: TechnicalDetailsSectionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <section className="technical-details-section">
      <button
        type="button"
        className="technical-details-header"
        onClick={() => setIsOpen((open) => !open)}
        aria-expanded={isOpen}
      >
        <div className="technical-details-header-text">
          <h2>Day {day}</h2>
          <p>Model technical details</p>
        </div>

        <span
          className={`technical-details-chevron ${
            isOpen ? "is-open" : ""
          }`}
          aria-hidden="true"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="m6 9 6 6 6-6" />
          </svg>
        </span>
      </button>

      <div
        className={`technical-details-content ${
          isOpen ? "is-open" : ""
        }`}
      >
        <div className="technical-details-content-inner">
          {children}
        </div>
      </div>
    </section>
  );
}

export default TechnicalDetailsSection;