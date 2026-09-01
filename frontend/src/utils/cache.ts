type CacheEntry<T> = {
  expiresAt: string;
  data: T;
};

export function readCache<T>(
  key: string,
): CacheEntry<T> | null {
  const cached = localStorage.getItem(key);

  if (!cached) {
    return null;
  }

  try {
    return JSON.parse(cached) as CacheEntry<T>;
  } catch {
    localStorage.removeItem(key);
    return null;
  }
}

export function readValidCache<T>(
  key: string,
): T | null {
  const cache = readCache<T>(key);

  if (!cache) {
    return null;
  }

  if (new Date(cache.expiresAt) <= new Date()) {
    localStorage.removeItem(key);
    return null;
  }

  return cache.data;
}

export function saveCache<T>(
  key: string,
  data: T,
  expiresAt: Date,
): void {
  const cache: CacheEntry<T> = {
    expiresAt: expiresAt.toISOString(),
    data,
  };

  localStorage.setItem(
    key,
    JSON.stringify(cache),
  );
}