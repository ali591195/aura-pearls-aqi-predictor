import numpy as np
import shap

from src.common.constants import (
    ALL_LOG_TRANSFORM_FEATURES,
    ALL_TRAINING_FEATURES,
    CURRENT_PROD_MODELS,
    LATEST_SELECTED_FEATURES_LIST,
    TARGET_COLUMNS
)
from src.common.hopsworks_client import mr

from backend.app.services.feature_service import get_features
from backend.app.services.model_service import get_models, get_scaler
from backend.app.schemas.technical_details import (
    ModelMetrics,
    ModelTechnicalDetails,
    SHAPFeature,
    TechnicalDetailsResponse,
)


def _get_latest_version(model_name: str):
    model_versions = mr.get_models(model_name)

    return max(
        model_versions,
        key=lambda model: model.version
    )


def _get_local_shap(
    model,
    model_type: str,
    feature_data,
    feature_list: list[str],
    scaler,
) -> list[SHAPFeature]:
    """
    Generate local SHAP values for the current prediction.
    """

    if model_type == "MLP":
        df_preprocess = feature_data.copy()

        for feature in ALL_LOG_TRANSFORM_FEATURES:
            df_preprocess[feature] = np.log1p(
                df_preprocess[feature]
            )

        df_preprocess[ALL_TRAINING_FEATURES] = scaler.transform(
            df_preprocess[ALL_TRAINING_FEATURES]
        )

        X = df_preprocess[feature_list].to_numpy()

        # Median point after RobustScaler transformation.
        background = np.zeros(
            (1, len(feature_list)),
            dtype=float,
        )

        explainer = shap.DeepExplainer(
            model,
            background,
        )

        shap_values = explainer.shap_values(X)

        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        shap_values = np.asarray(shap_values)

        if shap_values.ndim == 3:
            shap_values = shap_values[0, :, 0]
        else:
            shap_values = shap_values[0]

        values = X[0]

    else:
        X = feature_data[feature_list]

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        shap_values = np.asarray(shap_values)

        if shap_values.ndim > 1:
            shap_values = shap_values[0]

        values = X.iloc[0].to_numpy()

    return [
        SHAPFeature(
            feature=feature,
            value=float(value),
            shap_value=float(shap_value),
        )
        for feature, value, shap_value in zip(
            feature_list,
            values,
            shap_values,
        )
    ]


def get_technical_details() -> TechnicalDetailsResponse:
    """
    Get production model metadata, metrics and local SHAP explanations.
    """

    features = get_features()
    models = get_models()
    scaler = get_scaler()

    model_details = []

    for i, ((model, model_type), model_config) in enumerate(
        zip(models, CURRENT_PROD_MODELS)
    ):
        model_name = model_config[0]
        feature_list = LATEST_SELECTED_FEATURES_LIST[i]

        model_version = _get_latest_version(model_name)

        training_metrics = model_version.training_metrics or {}

        metrics = ModelMetrics(
            rmse=float(training_metrics["rmse"]),
            mae=float(training_metrics["mae"]),
            r2=float(training_metrics["r2"]),
        )

        shap_features = _get_local_shap(
            model=model,
            model_type=model_type,
            feature_data=features,
            feature_list=feature_list,
            scaler=scaler,
        )

        model_details.append(
            ModelTechnicalDetails(
                model_name=model_name,
                model_type=model_type,
                target=__import__(
                    "src.common.constants",
                    fromlist=["TARGET_COLUMNS"],
                ).TARGET_COLUMNS[i],
                version=model_version.version,
                metrics=metrics,
                shap=shap_features,
            )
        )

    return TechnicalDetailsResponse(
        models=model_details
    )