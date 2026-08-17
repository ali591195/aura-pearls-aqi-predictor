from src.engineered_features.data_utils import run_engineered_features_pipeline


def run_weekly_engineered_recovery():
    """
        Run the weekly engineering recovery pipeline

        :return: None
    """

    run_engineered_features_pipeline("WEEKLY_RECOVERY")

