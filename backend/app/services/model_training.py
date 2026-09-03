from backend.app.schemas.model_training import ModelTrainingResponse
from src.model_training.model_training import run_model_training


def train_models() -> ModelTrainingResponse:
    """
    Run model training using the latest engineered historical data.
    """

    run_model_training()

    return ModelTrainingResponse(
        message="Model training completed successfully."
    )