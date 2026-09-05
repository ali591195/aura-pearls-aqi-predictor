from typing import Any

from pydantic import BaseModel


class SHAPFeature(BaseModel):
    feature: str
    value: float
    shap_value: float


class ModelMetrics(BaseModel):
    rmse: float
    mae: float
    r2: float


class ModelTechnicalDetails(BaseModel):
    model_name: str
    model_type: str
    target: str
    version: int
    metrics: ModelMetrics
    shap: list[SHAPFeature]


class TechnicalDetailsResponse(BaseModel):
    models: list[ModelTechnicalDetails]