export function formatCurrentDateTime(
  ts: string,
): string {
  return new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Karachi",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  }).format(new Date(ts));
}

export function formatDate(
  date: Date | string,
): string {
  return new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Karachi",
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(
    typeof date === "string"
      ? new Date(date)
      : date,
  );
}

export function getForecastDate(
  baseDate: Date,
  forecastDay: number,
): string {
  const forecastDate = new Date(baseDate);

  forecastDate.setUTCDate(
    forecastDate.getUTCDate() + forecastDay,
  );

  return formatDate(forecastDate);
}

export function getDay1Label(
  baseDate: Date,
): string {
  const yesterday = new Date();

  yesterday.setUTCHours(0, 0, 0, 0);
  yesterday.setUTCDate(
    yesterday.getUTCDate() - 1,
  );

  const base = new Date(baseDate);

  base.setUTCHours(0, 0, 0, 0);

  if (base.getTime() === yesterday.getTime()) {
    return "Today";
  }

  return getForecastDate(baseDate, 1);
}