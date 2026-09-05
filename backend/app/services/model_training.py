import importlib

from backend.app.schemas.model_training import ModelTrainingResponse
import src.model_training.model_training as model_training

def train_models() -> ModelTrainingResponse:
    """
    Run model training using the latest engineered historical data.
    """

    importlib.reload(model_training)

    model_training.run_model_training()

    return ModelTrainingResponse(
        message="Model training completed successfully."
    )