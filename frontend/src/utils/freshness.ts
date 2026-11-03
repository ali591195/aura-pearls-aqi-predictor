function toLocalDay(
  date: Date | string,
): Date | null {
  const day = new Date(date);

  if (Number.isNaN(day.getTime())) {
    return null;
  }

  day.setHours(0, 0, 0, 0);

  return day;
}

/**
 * A prediction is fresh when its `ts` (date of the latest engineered
 * feature row) falls on yesterday or later, in local calendar days.
 * An invalid `ts` is never fresh.
 */
export function isPredictionFresh(
  ts: Date | string,
): boolean {
  const predictionDay = toLocalDay(ts);

  if (predictionDay === null) {
    return false;
  }

  const yesterday = new Date();
  yesterday.setHours(0, 0, 0, 0);
  yesterday.setDate(yesterday.getDate() - 1);

  return predictionDay >= yesterday;
}

/**
 * The local calendar day the prediction's day 1 targets (`ts` + 1 day).
 * Returns null when `ts` is not a valid date.
 */
export function getPredictionTargetDate(
  ts: Date | string,
): Date | null {
  const targetDay = toLocalDay(ts);

  if (targetDay === null) {
    return null;
  }

  targetDay.setDate(targetDay.getDate() + 1);

  return targetDay;
}
