from src.engineered_features.data_utils import run_engineered_features_pipeline


def run_monthly_engineered_recovery():
    """
        Run the monthly engineering recovery pipeline

        :return: None
    """
    run_engineered_features_pipeline("MONTHLY_RECOVERY")

