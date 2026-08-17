from src.common.constants import TARGET_COLUMNS
from src.common.hopsworks_client import insert_engineered_features
from src.engineered_features.data_utils import get_complete_raw_data, build_daily_engineered_features


def run_daily_pipeline():
    """
            Run the daily engineering pipeline

            :return: None
    """

    # Get raw data
    df, yesterday = get_complete_raw_data("NORMAL")

    # Engineer features
    engineered_features_dict = build_daily_engineered_features(df, yesterday)

    # Insert in data store
    insert_engineered_features([engineered_features_dict], TARGET_COLUMNS)