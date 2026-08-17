# from datetime import datetime, UTC
#
# from src.backfill.engineered_features_backfill import run_engineered_features_backfill
# from src.backfill.historical_backfill import run_historical_backfill
from src.common.hopsworks_client import engineered_daily_fs, raw_hourly_fs
# import pandas as pd
#
df = engineered_daily_fs.read()

print(df.shape)
#
# expected_dates = pd.date_range(
#     start="2022-08-11",
#     end="2026-08-16",
#     freq="D",
#     tz="UTC"
# )
#
# actual_dates = pd.to_datetime(df["ts"]).dt.normalize()
#
# missing_dates = expected_dates.difference(actual_dates)
#
# print(missing_dates)

# date_ranges = [
    # ("2023-05-04", "2023-05-07"),
    # ("2023-12-31", "2024-01-03"),
    # ("2024-08-27", "2024-08-30"),
#     ("2025-04-23", "2025-04-26"),
# ]
#
# for start_date, end_date in date_ranges:
#     run_engineered_features_backfill(
#         datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=UTC),
#         datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=UTC)
#     )