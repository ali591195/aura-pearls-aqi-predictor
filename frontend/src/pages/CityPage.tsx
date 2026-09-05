import { useState } from "react";

import PageHeader from "../components/common/PageHeader.tsx";

import PredictionCards from "../components/prediction/PredictionCards.tsx";

import AirQualitySection from "../components/stats/AirQualitySection.tsx";
import AirQualityGrid from "../components/stats/AirQualityGrid.tsx";
import TodayPredictionCard from "../components/stats/TodayPredictionCard.tsx";
import AQIOverviewCards from "../components/stats/AQIOverviewCards.tsx";
import PollutantCard from "../components/stats/PollutantCard.tsx";

import WeatherSection from "../components/stats/WeatherSection.tsx";
import WeatherOverviewCards from "../components/stats/WeatherOverviewCards.tsx";

import CitySearchCard from "../components/city/CitySearchCard.tsx";
import CityLoadingSkeleton from "../components/city/CityLoadingSkeleton.tsx";

import useCity from "../hooks/useCity";
import SectionHeader from "../components/common/SectionHeader.tsx";
import CityModelNotice from "../components/city/CityModelNotice.tsx";

function CityPage() {
  const {
    data,
    loading,
    error,
    submitCity,
  } = useCity();

  const [location, setLocation] =
    useState<{
      latitude: number;
      longitude: number;
    } | null>(null);

  function handleSubmit(
    latitude: number,
    longitude: number,
  ) {
    setLocation({
      latitude,
      longitude,
    });

    void submitCity(
      latitude,
      longitude,
    );
  }

  const prediction =
    data?.prediction ?? null;

  const currentAirQuality =
    data?.current_air_quality ?? null;

  const currentWeather =
    data?.current_weather ?? null;

  const pollutantRows =
    currentAirQuality
      ? [
          [
            {
              name: "PM10",
              value:
                currentAirQuality.pm10,
              unit:
                currentAirQuality.unit_pm10,
            },
            {
              name: "PM2.5",
              value:
                currentAirQuality.pm2_5,
              unit:
                currentAirQuality.unit_pm2_5,
            },
            {
              name: "CO",
              value:
                currentAirQuality.carbon_monoxide,
              unit:
                currentAirQuality.unit_carbon_monoxide,
            },
          ],
          [
            {
              name: "NO₂",
              value:
                currentAirQuality.nitrogen_dioxide,
              unit:
                currentAirQuality.unit_nitrogen_dioxide,
            },
            {
              name: "SO₂",
              value:
                currentAirQuality.sulphur_dioxide,
              unit:
                currentAirQuality.unit_sulphur_dioxide,
            },
            {
              name: "O₃",
              value:
                currentAirQuality.ozone,
              unit:
                currentAirQuality.unit_ozone,
            },
          ],
        ]
      : [];

  const weatherMetrics =
    currentWeather
      ? [
          {
            name: "Pressure",
            value:
              currentWeather.pressure,
            unit:
              currentWeather.unit_pressure,
          },
          {
            name: "Wind Speed",
            value:
              currentWeather.wind_speed,
            unit:
              currentWeather.unit_wind_speed,
          },
          {
            name: "Dew Point",
            value:
              currentWeather.dew_point,
            unit:
              currentWeather.unit_dew_point,
          },
        ]
      : [];

  const subtitle = location
    ? `${location.latitude.toFixed(4)}, ${location.longitude.toFixed(4)}`
    : "Enter coordinates";

  return (
    <>
      <PageHeader
        title="City"
        subtitle={subtitle}
      />

      <CityModelNotice />

      <CitySearchCard
        onSubmit={handleSubmit}
        loading={loading}
      />

      {error && !loading && (
        <p>{error}</p>
      )}

      {loading && (
        <CityLoadingSkeleton />
      )}

      {!loading &&
        prediction &&
        currentAirQuality &&
        currentWeather && (
          <>
            <SectionHeader
              title="Air Quality Forecast"
              subtitle="Predicted AQI for the upcoming days"
            />

            <PredictionCards
              data={prediction}
            />

            <AirQualitySection>
              <AirQualityGrid>
                <div className="air-quality-grid-row air-quality-grid-row-aqi">
                  <TodayPredictionCard
                    data={prediction} toggle_notice={false}
                  />

                  <AQIOverviewCards
                    data={currentAirQuality}
                  />
                </div>

                {pollutantRows.map(
                  (row, rowIndex) => (
                    <div
                      className="air-quality-grid-row air-quality-grid-row-pollutants"
                      key={rowIndex}
                    >
                      {row.map(
                        (pollutant) => (
                          <PollutantCard
                            key={
                              pollutant.name
                            }
                            name={
                              pollutant.name
                            }
                            value={
                              pollutant.value!
                            }
                            unit={
                              pollutant.unit!
                            }
                            timestamp={
                              currentAirQuality.ts
                            }
                          />
                        ),
                      )}
                    </div>
                  ),
                )}
              </AirQualityGrid>
            </AirQualitySection>

            <WeatherSection>
              <WeatherOverviewCards
                data={currentWeather}
              />

              <div className="air-quality-grid-row air-quality-grid-row-pollutants">
                {weatherMetrics.map(
                  (metric) => (
                    <PollutantCard
                      key={metric.name}
                      name={metric.name}
                      value={metric.value}
                      unit={metric.unit}
                      timestamp={
                        currentWeather.ts
                      }
                    />
                  ),
                )}
              </div>
            </WeatherSection>
          </>
        )}
    </>
  );
}

export default CityPage;

