from datetime import datetime, UTC, timedelta

from pandas import DataFrame

from src.common.constants import OPENMETEO_WEATHER_URL, TARGET_COLUMNS, HISTORICAL_BACKFILL_START_DATE
from src.common.hopsworks_client import raw_hourly_fs, insert_engineered_features
from src.common.schemas import EngineeredFeatureDict, FeatureEngineeringMode
from src.feature_pipeline.daily_recovery import run_daily_recovery
from src.feature_pipeline.data_collector import collect_and_insert_features


def get_complete_raw_data(mode: FeatureEngineeringMode, backfill_start_date: datetime | None = None) -> tuple[DataFrame, datetime | tuple[datetime, datetime]] | None:
    """
        Get raw data from feature store for engineering pipelines

        :param mode: Recovery, normal or backfill mode
        :param backfill_start_date: Start date for backfill mode
        :return: The raw data and yesterday's datetime or a range of datetime
    """

    today = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)

    # Dates
    yesterday = today - timedelta(days=1)
    start_date = yesterday - timedelta(days=6)
    end_date = today
    prev_days_start = yesterday

    if mode == "WEEKLY_RECOVERY":
        prev_days_start = yesterday - timedelta(days=6)
        start_date = prev_days_start - timedelta(days=6)


    elif mode == "MONTHLY_RECOVERY":
        prev_days_start = yesterday - timedelta(days=29)
        start_date = prev_days_start - timedelta(days=6)


    elif mode == "BACKFILL":
        if backfill_start_date is None:
            backfill_start_date = datetime.strptime(
                HISTORICAL_BACKFILL_START_DATE,
                "%Y-%m-%d"
            ).replace(tzinfo=UTC)

        prev_days_start = backfill_start_date + timedelta(days=6)
        start_date = prev_days_start - timedelta(days=6)



    expected_rows = int(
        (today - prev_days_start).total_seconds() / 3600
    )

    # Data extraction
    df = raw_hourly_fs.read(
        start_time=start_date,
        end_time=end_date
    )

    # Complete data evaluation (mode dependent)
    if mode == "NORMAL":
        required_rows = df[df["ts"].dt.date == yesterday.date()]

    elif mode == "WEEKLY_RECOVERY" or mode == "MONTHLY_RECOVERY" or mode == "BACKFILL":
        required_rows = df[
            (df["ts"] >= prev_days_start) &
            (df["ts"] < today)
            ]


    if len(required_rows) != expected_rows:

        if mode == "WEEKLY_RECOVERY" or mode == "MONTHLY_RECOVERY":
            date_range = (
                prev_days_start.strftime("%Y-%m-%d"),
                yesterday.strftime("%Y-%m-%d")
            )

            collect_and_insert_features(OPENMETEO_WEATHER_URL, "BACKFILL", date_range)

        elif mode == "NORMAL":
            run_daily_recovery()

        elif mode == "BACKFILL":
            print("Not enough rows. First, run historical backfill manually on the current range. Then, try again.")
            return None

        df = raw_hourly_fs.read(
            start_time=start_date,
            end_time=end_date
        )

    engineering_period = yesterday

    # For recovery, get a range of dates
    if mode == "WEEKLY_RECOVERY" or mode == "MONTHLY_RECOVERY" or mode == "BACKFILL":
        engineering_period = (prev_days_start, yesterday)

    return df, engineering_period

def build_daily_engineered_features(df: DataFrame, date: datetime) -> EngineeredFeatureDict:
    """
        Build Engineered Features for a single day

        :param df: The required dataframe.
        :param date: The date for which we are engineering.
        :return: The engineered features.
    """

    daily_df = df.groupby(df["ts"].dt.date).mean(numeric_only=True)

    # Lag dates
    day_lag_1 = (date - timedelta(days=1))
    day_lag_2 = (day_lag_1 - timedelta(days=1))
    day_lag_3 = (day_lag_2 - timedelta(days=1))

    # Data
    date_df = daily_df.loc[date.date()]
    lag_1 = daily_df.loc[day_lag_1.date()]
    lag_2 = daily_df.loc[day_lag_2.date()]
    lag_3 = daily_df.loc[day_lag_3.date()]

    aqi_today = date_df["aqi"]
    aqi_lag_1 = lag_1["aqi"]

    day_of_week = date.weekday()
    is_weekend = day_of_week >= 5

    # Engineered Features
    engineered_features_dict: EngineeredFeatureDict = {
        # AQI
        "aqi_today": aqi_today,
        "aqi_lag_1": aqi_lag_1,
        "aqi_lag_2": lag_2["aqi"],
        "aqi_lag_3": lag_3["aqi"],
        "aqi_roll_mean_3": daily_df["aqi"].rolling(3).mean().loc[date.date()],
        "aqi_roll_mean_7": daily_df["aqi"].rolling(7).mean().loc[date.date()],
        "aqi_roll_std_3": daily_df["aqi"].rolling(3).std().loc[date.date()],
        "aqi_roll_std_7": daily_df["aqi"].rolling(7).std().loc[date.date()],
        "aqi_change_rate": aqi_today - aqi_lag_1,

        # Pollutants
        "pm25_today": date_df["pm25"],
        "pm10_today": date_df["pm10"],
        "o3_today": date_df["o3"],
        "co_today": date_df["co"],
        "no2_today": date_df["no2"],
        "so2_today": date_df["so2"],

        # Weather
        "temp_today": date_df["temp"],
        "pressure_today": date_df["pressure"],
        "humidity_today": date_df["humidity"],
        "wind_spd_today": date_df["wind_spd"],
        "dew_pt_today": date_df["dew_pt"],

        # Lag Pollutants
        "pm25_lag_1": lag_1["pm25"],
        "pm10_lag_1": lag_1["pm10"],
        "o3_lag_1": lag_1["o3"],

        "pm25_lag_2": lag_2["pm25"],
        "pm10_lag_2": lag_2["pm10"],
        "o3_lag_2": lag_2["o3"],

        "pm25_lag_3": lag_3["pm25"],
        "pm10_lag_3": lag_3["pm10"],
        "o3_lag_3": lag_3["o3"],

        # Lag Weather
        "temp_lag_1": lag_1["temp"],
        "pressure_lag_1": lag_1["pressure"],
        "humidity_lag_1": lag_1["humidity"],
        "wind_spd_lag_1": lag_1["wind_spd"],
        "dew_pt_lag_1": lag_1["dew_pt"],

        # Roll Mean
        "pm25_roll_mean_3": daily_df["pm25"].rolling(3).mean().loc[date.date()],
        "pm25_roll_mean_7": daily_df["pm25"].rolling(7).mean().loc[date.date()],
        "pm10_roll_mean_3": daily_df["pm10"].rolling(3).mean().loc[date.date()],
        "pm10_roll_mean_7": daily_df["pm10"].rolling(7).mean().loc[date.date()],
        "o3_roll_mean_3": daily_df["o3"].rolling(3).mean().loc[date.date()],
        "o3_roll_mean_7": daily_df["o3"].rolling(7).mean().loc[date.date()],

        # Roll Standard Deviation
        "pm25_roll_std_3": daily_df["pm25"].rolling(3).std().loc[date.date()],
        "pm25_roll_std_7": daily_df["pm25"].rolling(7).std().loc[date.date()],
        "pm10_roll_std_3": daily_df["pm10"].rolling(3).std().loc[date.date()],
        "pm10_roll_std_7": daily_df["pm10"].rolling(7).std().loc[date.date()],
        "o3_roll_std_3": daily_df["o3"].rolling(3).std().loc[date.date()],
        "o3_roll_std_7": daily_df["o3"].rolling(7).std().loc[date.date()],

        # Calendar
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "month": date.month,

        # Target Features
        "target_aqi_day1": None,
        "target_aqi_day2": None,
        "target_aqi_day3": None,
        "target_aqi_day4": None,

        # Metadata
        "ts": date
    }

    return engineered_features_dict

def build_engineered_features_for_dates(df: DataFrame, dates: list[datetime]) -> list[EngineeredFeatureDict]:
    """
        Build Engineered Features for a specific duration

        :param df: The required dataframe.
        :param dates: The dates for which to build engineered features.
        :return: The engineered features.
    """

    engineered_features: list[EngineeredFeatureDict] = []

    # For each date in dates
    for i, date in enumerate(dates):
        # Engineer a single day's features
        engineered_dict = build_daily_engineered_features(df, date)

        # If they are not the last four days
        if i < len(dates) - 4:
            # List of next four dates
            target_dates = [dates[i + 1].date(), dates[i + 2].date(), dates[i + 3].date(), dates[i + 4].date()]

            # Grouped aqi means of each date
            aqi_means = (
                df[df["ts"].dt.date.isin(target_dates)]
                .groupby(df["ts"].dt.date)["aqi"]
                .mean()
            )

            # List of aqi means of each day
            target_aqi_means = [
                aqi_means.loc[target_date]
                for target_date in target_dates
            ]

            # For each column in target columns
            for j, target_column in enumerate(TARGET_COLUMNS):
                # Update that target column
                engineered_dict[target_column] = target_aqi_means[j]

        # Append the engineered features in a list
        engineered_features.append(engineered_dict)

    return engineered_features

def run_engineered_features_pipeline(mode: FeatureEngineeringMode, backfill_start_date: datetime | None = None) -> None:
    """
        Run the engineering recovery pipeline

        :param mode: Recovery, normal or backfill mode
        :param backfill_start_date: Start date for backfill mode
        :return: None
    """
    # Get raw data
    df, date_range = get_complete_raw_data(mode, backfill_start_date)

    # Get date ranges
    start_date, end_date = date_range

    # For each date
    dates = [
        start_date + timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
    ]

    engineered_features = build_engineered_features_for_dates(df, dates)

    # Insert in data store
    insert_engineered_features(engineered_features, TARGET_COLUMNS)