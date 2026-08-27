import subprocess
from pathlib import Path

import tensorflow as tf
from keras.src.callbacks import EarlyStopping

from src.common.constants import SELECTED_FEATURES_LIST, TARGET_COLUMNS, ALL_LOG_TRANSFORM_FEATURES, \
    ALL_TRAINING_FEATURES
from src.common.hopsworks_client import engineered_daily_fs, mr
from src.common.schemas import DeepLearningFitParamSchema
from src.model_training.data_utils import build_mlp_model
from src.modeling.data_utils import split_modeling_data, preprocess_data, train_and_evaluate_model, evaluate_model


ROOT_DIR = Path(
    subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
    ).strip()
)

MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

def run_model_training() -> None:
    """
        Run model training pipeline

        :return: None
    """
    # Get dataframe
    df = engineered_daily_fs.read()

    df = (
        df.dropna(subset=TARGET_COLUMNS)
        .sort_values("ts")
        .reset_index(drop=True)
    )

    # Split dataframe
    train_df, val_df, test_df = split_modeling_data(df)

    # Preprocess data
    train_df, val_df, test_df = preprocess_data(train_df, val_df, test_df, log_features=ALL_LOG_TRANSFORM_FEATURES,
                                                scale_features=ALL_TRAINING_FEATURES)

    tf.keras.utils.set_random_seed(42)

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=15,
        restore_best_weights=True,
    )

    mlp_base_model_fit_params: DeepLearningFitParamSchema = {
        "epochs": 500,
        "batch_size": 32,
        "callbacks": [early_stopping],
        "verbose": 1
    }

    # For each feature sets per model
    for i, features_list in enumerate(SELECTED_FEATURES_LIST):
        labels = [TARGET_COLUMNS[i]]
        total_features = len(features_list)

        # Get mlp model
        model = build_mlp_model(total_features)

        # Get metrics and train the model
        result = train_and_evaluate_model(
            train_df, val_df, disable_plot=True, baseline=features_list, model=model, output_labels=labels,
            toggle_evaluate_print=True, deep_learning=mlp_base_model_fit_params
        )

        # Get the trained model
        model = result[0]

        # Predict on test and get metrics
        X_test = test_df[features_list]

        y_test_pred = model.predict(X_test)

        y_test = test_df[labels].squeeze()

        rmse, mae, r2 = evaluate_model(y_test, y_test_pred, toggle_print=True, labels=labels)

        metrics = {
            "rmse": rmse[0],
            "mae": mae[0],
            "r2": r2[0],
        }

        # Saving model
        model_path = MODEL_DIR / f"aqi_mlp_day_{i + 1}.keras"
        model.save(model_path)

        # Creating meta data
        model_meta = mr.tensorflow.create_model(
            name=f"aqi_mlp_day_{i + 1}",
            metrics=metrics,
            description=f"AQI Day {i + 1} Predictor"
        )

        # Saving to model registry
        model_meta.save(str(model_path))
