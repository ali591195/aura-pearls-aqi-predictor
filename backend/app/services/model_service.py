import joblib
import shutil
import threading
import time
from pathlib import Path
from typing import Any, Callable

import lightgbm as lgb
from hsml.model import Model
from keras.src.saving import load_model
from sklearn.preprocessing import RobustScaler
from xgboost import XGBRegressor

from src.common.constants import MODEL_DIR, CURRENT_PROD_MODELS
from src.common.hopsworks_client import mr


# Registry lookups are slow (~4s each), so the latest version is re-checked at most every 10 minutes.
# Training through the API clears the cache, so a new version is picked up immediately.
VERSION_CHECK_INTERVAL_SECONDS = 600

# In-memory cache of loaded artifacts: model name -> (version, loaded object)
_cache: dict[str, tuple[int, Any]] = {}
# Latest registry version per model name: model name -> (checked at, model version object)
_version_cache: dict[str, tuple[float, Model]] = {}
_cache_lock = threading.Lock()


def _get_latest_version(model_name: str) -> Model:
    """
        Get latest model version, re-checking the registry at most
        every VERSION_CHECK_INTERVAL_SECONDS

        :param model_name: Model name
        :return: Model version object with the highest version number
    """

    cached = _version_cache.get(model_name)

    if cached is not None and time.monotonic() - cached[0] < VERSION_CHECK_INTERVAL_SECONDS:
        return cached[1]

    model_versions = mr.get_models(model_name)
    latest = max(model_versions, key=lambda model: model.version)

    _version_cache[model_name] = (time.monotonic(), latest)

    return latest


def clear_model_cache() -> None:
    """
        Forget cached versions and loaded artifacts, so the next request
        loads the latest models from the registry

        :return: None
    """

    with _cache_lock:
        _version_cache.clear()
        _cache.clear()


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


def _load_xgboost(model_path: Path) -> XGBRegressor:
    """
        Load an XGBoost model from disk

        :param model_path: Model file path
        :return: Loaded XGBRegressor
    """

    model = XGBRegressor()
    model.load_model(model_path)
    return model


# Model type -> (artifact file extension, loader)
_MODEL_LOADERS: dict[str, tuple[str, Callable[[Path], Any]]] = {
    "XGBoost": (".json", _load_xgboost),
    "MLP": (".keras", load_model),
    "LightGBM": (".txt", lambda path: lgb.Booster(model_file=path)),
    "Random Forest": (".joblib", joblib.load),
}


def _get_cached(
    model_name: str,
    artifact_name: str,
    loader: Callable[[Path], Any]
) -> Any:
    """
        Get a loaded artifact, reloading only when the registry has a newer version

        :param model_name: Model name in the registry
        :param artifact_name: Artifact file name inside the model directory
        :param loader: Function that loads the artifact from its path
        :return: Loaded artifact
    """

    model_version = _get_latest_version(model_name)
    version = model_version.version

    cached = _cache.get(model_name)
    if cached is not None and cached[0] == version:
        return cached[1]

    with _cache_lock:
        # Another thread may have loaded it while we waited
        cached = _cache.get(model_name)
        if cached is not None and cached[0] == version:
            return cached[1]

        model_dir = MODEL_DIR / model_name

        if not _is_version_downloaded(model_dir, artifact_name, version):
            if model_dir.exists():
                shutil.rmtree(model_dir)

            model_version.download(
                local_path=str(model_dir),
            )
            _save_version(model_dir, version)

        loaded = loader(model_dir / artifact_name)
        _cache[model_name] = (version, loaded)

        return loaded


def get_models() -> list[tuple[Any, str]]:
    """
    Get the latest model for each forecast day.

    :return: List of (model, model_type) tuples for days 1–4.
    """

    models = []

    for model_name, model_type in CURRENT_PROD_MODELS:
        if model_type not in _MODEL_LOADERS:
            raise ValueError(
                f"Unknown model type '{model_type}' for model '{model_name}'"
            )

        extension, loader = _MODEL_LOADERS[model_type]
        model = _get_cached(model_name, f"{model_name}{extension}", loader)

        models.append((model, model_type))

    return models


def get_scaler() -> RobustScaler:
    """
    Get the latest shared preprocessing scaler.

    :return: Latest fitted RobustScaler.
    """

    return _get_cached("aqi_preprocessor", "scaler.joblib", joblib.load)
