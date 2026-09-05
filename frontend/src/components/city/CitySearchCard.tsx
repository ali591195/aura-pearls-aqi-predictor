import {
    type SyntheticEvent,
  useState,
} from "react";

import "./CitySearchCard.css";

interface CitySearchCardProps {
  onSubmit: (
    latitude: number,
    longitude: number,
  ) => void;

  loading: boolean;
}

function CitySearchCard({
  onSubmit,
  loading,
}: CitySearchCardProps) {
  const [latitude, setLatitude] =
    useState("");

  const [longitude, setLongitude] =
    useState("");

  function handleSubmit(
    event: SyntheticEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const parsedLatitude =
      Number(latitude);

    const parsedLongitude =
      Number(longitude);

    if (
      !Number.isFinite(parsedLatitude) ||
      !Number.isFinite(parsedLongitude)
    ) {
      return;
    }

    if (
      parsedLatitude < -90 ||
      parsedLatitude > 90 ||
      parsedLongitude < -180 ||
      parsedLongitude > 180
    ) {
      return;
    }

    onSubmit(
      parsedLatitude,
      parsedLongitude,
    );
  }

  return (
    <section className="city-search-card">
      <form
        className="city-search-form"
        onSubmit={handleSubmit}
      >
        <div className="city-search-fields">
          <div className="city-search-field">
            <label htmlFor="city-latitude">
              Latitude
            </label>

            <input
              id="city-latitude"
              type="number"
              step="any"
              min="-90"
              max="90"
              placeholder="e.g. 31.5204"
              value={latitude}
              onChange={(event) =>
                setLatitude(event.target.value)
              }
              disabled={loading}
              required
            />

            <span>
              Range: −90 to 90
            </span>
          </div>

          <div className="city-search-field">
            <label htmlFor="city-longitude">
              Longitude
            </label>

            <input
              id="city-longitude"
              type="number"
              step="any"
              min="-180"
              max="180"
              placeholder="e.g. 74.3587"
              value={longitude}
              onChange={(event) =>
                setLongitude(event.target.value)
              }
              disabled={loading}
              required
            />

            <span>
              Range: −180 to 180
            </span>
          </div>
        </div>

        <div className="city-search-action">
          <button
            type="submit"
            className="city-search-submit"
            disabled={loading}
          >
            {loading
              ? "Loading..."
              : "Get City Data"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default CitySearchCard;