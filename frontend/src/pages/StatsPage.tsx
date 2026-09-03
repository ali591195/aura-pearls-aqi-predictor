import useCurrentAirQuality from "../hooks/useCurrentAirQuality";
import usePrediction from "../hooks/usePrediction";
import PageHeader from "../components/common/PageHeader.tsx";
import AirQualitySection from "../components/stats/AirQualitySection.tsx";
import AirQualityGrid from "../components/stats/AirQualityGrid.tsx";
import TodayPredictionCard from "../components/stats/TodayPredictionCard.tsx";
import AQIOverviewCards from "../components/stats/AQIOverviewCards.tsx";
import PollutantCard from "../components/stats/PollutantCard.tsx";
import WeatherSection from "../components/stats/WeatherSection.tsx";
import useCurrentWeather from "../hooks/useCurrentWeather.ts";
import WeatherOverviewCards from "../components/stats/WeatherOverviewCards.tsx";

function StatsPage() {
  const {
    data: currentAirQuality,
    loading: currentAirQualityLoading,
    error: currentAirQualityError,
  } = useCurrentAirQuality();

  const {
    prediction,
    loading: predictionLoading,
  } = usePrediction();

  const {
    data: currentWeather,
    loading: currentWeatherLoading,
    error: currentWeatherError,
  } = useCurrentWeather();

  const loading =
  currentAirQualityLoading ||
  predictionLoading ||
  currentWeatherLoading;

  const pollutantRows = currentAirQuality
  ? [
      [
        {
          name: "PM10",
          value: currentAirQuality.pm10,
          unit: currentAirQuality.unit_pm10,
        },
        {
          name: "PM2.5",
          value: currentAirQuality.pm2_5,
          unit: currentAirQuality.unit_pm2_5,
        },
        {
          name: "CO",
          value: currentAirQuality.carbon_monoxide,
          unit: currentAirQuality.unit_carbon_monoxide,
        },
      ],
      [
        {
          name: "NO₂",
          value: currentAirQuality.nitrogen_dioxide,
          unit: currentAirQuality.unit_nitrogen_dioxide,
        },
        {
          name: "SO₂",
          value: currentAirQuality.sulphur_dioxide,
          unit: currentAirQuality.unit_sulphur_dioxide,
        },
        {
          name: "O₃",
          value: currentAirQuality.ozone,
          unit: currentAirQuality.unit_ozone,
        },
      ],
    ]
  : [];

  const weatherMetrics = currentWeather
  ? [
      {
        name: "Pressure",
        value: currentWeather.pressure,
        unit: currentWeather.unit_pressure,
      },
      {
        name: "Wind Speed",
        value: currentWeather.wind_speed,
        unit: currentWeather.unit_wind_speed,
      },
      {
        name: "Dew Point",
        value: currentWeather.dew_point,
        unit: currentWeather.unit_dew_point,
      },
    ]
  : [];

  return (
    <>
      <PageHeader
        title="Statistics"
        subtitle="Lahore"
      />

      <AirQualitySection>
        <AirQualityGrid>
          {loading && (
            <p>Loading air quality...</p>
          )}

          {currentAirQualityError && (
            <p>{currentAirQualityError}</p>
          )}

          {!loading &&
            !currentAirQualityError &&
            prediction &&
            currentAirQuality && (
              <>
                <div className="air-quality-grid-row air-quality-grid-row-aqi">
                  <TodayPredictionCard
                    data={prediction}
                  />

                  <AQIOverviewCards
                    data={currentAirQuality}
                  />
                </div>

                {pollutantRows.map((row, rowIndex) => (
                  <div
                    className="air-quality-grid-row air-quality-grid-row-pollutants"
                    key={rowIndex}
                  >
                    {row.map((pollutant) => (
                      <PollutantCard
                        key={pollutant.name}
                        name={pollutant.name}
                        value={pollutant.value!}
                        unit={pollutant.unit!}
                        timestamp={currentAirQuality!.ts}
                      />
                    ))}
                  </div>
                ))}
              </>
            )}
        </AirQualityGrid>
      </AirQualitySection>
      <WeatherSection>
        {currentWeatherLoading && (
          <p>Loading weather...</p>
        )}

        {currentWeatherError && (
          <p>{currentWeatherError}</p>
        )}

        {!currentWeatherLoading &&
          !currentWeatherError &&
          currentWeather && (
            <>
              <WeatherOverviewCards
              data={currentWeather}
              />
              <div className="air-quality-grid-row air-quality-grid-row-pollutants">
                {weatherMetrics.map((metric) => (
                  <PollutantCard
                    key={metric.name}
                    name={metric.name}
                    value={metric.value}
                    unit={metric.unit}
                    timestamp={currentWeather!.ts}
                  />
                ))}
              </div>
            </>
          )}
      </WeatherSection>
    </>
  );
}

export default StatsPage;