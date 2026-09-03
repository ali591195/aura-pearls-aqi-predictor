from fastapi import APIRouter

from backend.app.schemas.model_training import ModelTrainingResponse
from backend.app.services.model_training import train_models
from backend.app.utils.routes import raise_internal_server_error

router = APIRouter(
    prefix="/api/model",
    tags=["Model"],
)


@router.post(
    "/train",
    response_model=ModelTrainingResponse,
)
def run_model_training_route() -> (
    ModelTrainingResponse | None
):
    try:
        return train_models()

    except RuntimeError as error:
        raise_internal_server_error(error)