from datetime import datetime

from src.engineered_features.data_utils import run_engineered_features_pipeline

def run_engineered_features_backfill(backfill_start_date: datetime | None = None, backfill_end_date: datetime | None = None):
    """
        Run the engineered backfill pipeline

        :param backfill_start_date: Start date for backfill mode
        :param backfill_end_date: End date for backfill mode
        :return: None
    """
    run_engineered_features_pipeline("BACKFILL", backfill_start_date, backfill_end_date)