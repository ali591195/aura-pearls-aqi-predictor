from fastapi import APIRouter

from backend.app.schemas.prediction import AQIPredictionResponse
from backend.app.services.feature_service import get_features
from backend.app.services.model_service import get_models, get_scaler
from backend.app.services.prediction_service import get_prediction

router = APIRouter(
    prefix="/api",
    tags=["Prediction"]
)


@router.get(
    "/prediction",
    response_model=AQIPredictionResponse
)
def predict() -> AQIPredictionResponse:
    features = get_features()
    models = get_models()
    scaler = get_scaler()

    predictions = get_prediction(features, models, scaler)

    for i, prediction in enumerate(predictions):
        predictions[i] = prediction.flatten()

    return AQIPredictionResponse(
        aqi_pred_day_1=predictions[0][0],
        aqi_pred_day_2=predictions[1][0],
        aqi_pred_day_3=predictions[2][0],
        aqi_pred_day_4=predictions[3][0],
        ts=features['ts'].iloc[0]
    )