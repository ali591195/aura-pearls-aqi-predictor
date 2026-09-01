export async function fetchApi<T>(
  url: string,
  errorMessage: string,
): Promise<T> {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(
      `${errorMessage}: ${response.status}`,
    );
  }

  return response.json() as Promise<T>;
}

export function getBackendApiUrl(
  endpoint: string,
): string {
  const backendHost =
    import.meta.env.VITE_BACKEND_HOST;

  const backendPort =
    import.meta.env.VITE_BACKEND_PORT;

  const baseUrl = backendPort
    ? `http://${backendHost}:${backendPort}`
    : `https://${backendHost}`;

  return `${baseUrl}${endpoint}`;
}