export type AQICategory = {
  label: string;
  className: string;
};

export function getAQICategory(
  value: number,
): AQICategory {
  if (value <= 50) {
    return {
      label: "Good",
      className: "aqi-good",
    };
  }

  if (value <= 100) {
    return {
      label: "Moderate",
      className: "aqi-moderate",
    };
  }

  if (value <= 150) {
    return {
      label: "Unhealthy for Sensitive Groups",
      className: "aqi-sensitive",
    };
  }

  if (value <= 200) {
    return {
      label: "Unhealthy",
      className: "aqi-unhealthy",
    };
  }

  if (value <= 300) {
    return {
      label: "Very Unhealthy",
      className: "aqi-very-unhealthy",
    };
  }

  return {
    label: "Hazardous",
    className: "aqi-hazardous",
  };
}

export function AQISymbol({
  value,
}: {
  value: number;
}) {
  if (value <= 50) {
    return (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <path d="M5 13l4 4L19 7" />
      </svg>
    );
  }

  if (value <= 100) {
    return (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        aria-hidden="true"
      >
        <path d="M5 12h14" />
      </svg>
    );
  }

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
      <path d="M12 3 2.8 20h18.4L12 3Z" />
      <path d="M12 9v5" />
      <circle
        cx="12"
        cy="17.2"
        r="0.7"
        fill="currentColor"
      />
    </svg>
  );
}