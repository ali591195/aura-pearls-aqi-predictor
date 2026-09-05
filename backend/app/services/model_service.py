import joblib
import shutil
from pathlib import Path

import lightgbm as lgb
from keras import Sequential
from keras.src.saving import load_model
from sklearn.preprocessing import RobustScaler
from xgboost.sklearn import XGBRegressor

from src.common.constants import MODEL_DIR, CURRENT_PROD_MODELS
from src.common.hopsworks_client import mr


def _get_latest_version(model_name: str) -> int:
    """
        Get latest model version

        :param model_name: Model name
        :return: Max version
    """

    model_versions = mr.get_models(model_name)
    return max(model_versions, key=lambda model: model.version)


def _is_version_downloaded(
    model_dir: Path,
    artifact_name: str,
    version: int
) -> bool:
    """
        Check if latest version downloaded or not

        :param model_dir: Model directory
        :param artifact_name: Artifact name
        :param version: Version number
        :return: Boolean value
    """

    artifact_path = model_dir / artifact_name
    version_file = model_dir / ".version"

    if not artifact_path.exists() or not version_file.exists():
        return False

    return int(version_file.read_text()) == version


def _save_version(model_dir: Path, version: int) -> None:
    """
        Save version file

        :param model_dir: Model directory
        :param version: Version number
        :return: None
    """

    (model_dir / ".version").write_text(str(version))


def get_models() -> list[Sequential]:
    """
    Get the latest model for each forecast day.

    :return: List of latest Sequential models for days 1–4.
    """

    models = []

    for model_tuple in CURRENT_PROD_MODELS:
        model_name, model_type = model_tuple
        model_version = _get_latest_version(model_name)

        model_dir = MODEL_DIR / model_name

        if model_type == "XGBoost":
            artifact_name = f"{model_name}.json"
        elif model_type == "MLP":
            artifact_name = f"{model_name}.keras"
        elif model_type == "LightGBM":
            artifact_name = f"{model_name}.txt"
        elif model_type == "Random Forest":
            artifact_name = f"{model_name}.joblib"

        if not _is_version_downloaded(
                model_dir,
                artifact_name,
                model_version.version
        ):
            if model_dir.exists():
                shutil.rmtree(model_dir)

            model_version.download(
                local_path=str(model_dir),
            )
            _save_version(model_dir, model_version.version)

        model_path = model_dir / artifact_name

        if model_type == "XGBoost":
            model = XGBRegressor()
            model.load_model(model_path)
        elif model_type == "MLP":
            model = load_model(model_path)
        elif model_type == "LightGBM":
            model = lgb.Booster(
                model_file=model_path
            )
        elif model_type == "Random Forest":
            model = joblib.load(model_path)

        models.append((model, model_type))

    return models


def get_scaler() -> RobustScaler:
    """
    Get the latest shared preprocessing scaler.

    :return: Latest fitted RobustScaler.
    """

    model_name = "aqi_preprocessor"
    model_version = _get_latest_version(model_name)

    preprocessor_dir = MODEL_DIR / model_name

    artifact_name = "scaler.joblib"

    if not _is_version_downloaded(
            preprocessor_dir,
            artifact_name,
            model_version.version
    ):
        if preprocessor_dir.exists():
            shutil.rmtree(preprocessor_dir)

        model_version.download(
            local_path=str(preprocessor_dir),
        )
        _save_version(preprocessor_dir, model_version.version)

    return joblib.load(preprocessor_dir / artifact_name)