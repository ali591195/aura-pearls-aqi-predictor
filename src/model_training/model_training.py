import joblib
import pandas as pd
import tensorflow as tf
from keras.src.callbacks import EarlyStopping

from src.common.constants import TARGET_COLUMNS, ALL_LOG_TRANSFORM_FEATURES, \
    ALL_TRAINING_FEATURES, MODEL_DIR, LATEST_SELECTED_FEATURES_LIST
from src.common.hopsworks_client import engineered_daily_fs, mr
from src.model_training.data_utils import fit_robust_scaler, get_day_1_model, get_day_2_model, \
    get_day_3_model, get_day_4_model
from src.modeling.data_utils import split_modeling_data, preprocess_data, evaluate_model


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

    train_df_copy = train_df.copy()

    # Get scaler
    scaler = fit_robust_scaler(train_df_copy, ALL_TRAINING_FEATURES)

    # Preprocess data
    train_df_preprocess, val_df_preprocess, test_df_preprocess = preprocess_data(train_df, val_df, test_df, log_features=ALL_LOG_TRANSFORM_FEATURES,
                                                scale_features=ALL_TRAINING_FEATURES)

    train_val_df = pd.concat(
        [train_df, val_df],
        axis=0,
    ).sort_values("ts").reset_index(drop=True)

    train_val_df_preprocess = pd.concat(
        [train_df_preprocess, val_df_preprocess],
        axis=0,
    ).sort_values("ts").reset_index(drop=True)

    tf.keras.utils.set_random_seed(42)

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=15,
        restore_best_weights=True,
    )

    models = []

    day_1_model = get_day_1_model()
    models.append((day_1_model, "XGBoost", "xgboost"))

    day_2_model = get_day_2_model()
    models.append((day_2_model, "MLP", "mlp"))

    day_3_model = get_day_3_model()
    models.append((day_3_model, "LightGBM", "lightgbm"))

    day_4_model = get_day_4_model()
    models.append((day_4_model, "Random Forest", "rf"))

    # For each feature sets per model
    for i, features_list in enumerate(LATEST_SELECTED_FEATURES_LIST):
        labels = [TARGET_COLUMNS[i]]

        if models[i][1] == "MLP":
            X_train = train_df_preprocess[features_list]
            y_train = train_df_preprocess[labels].to_numpy().ravel()

            X_val = val_df_preprocess[features_list]
            y_val = val_df_preprocess[labels].to_numpy().ravel()

            X_test = test_df_preprocess[features_list]
            y_test = test_df_preprocess[labels].to_numpy().ravel()

            models[i][0].fit(
                X_train,
                y_train,
                validation_data=(X_val, y_val),
                epochs=500,
                batch_size=32,
                callbacks=[early_stopping]
            )
        else:
            X_train = train_val_df[features_list]
            y_train = train_val_df[labels].to_numpy().ravel()

            X_test = test_df[features_list]
            y_test = test_df[labels].to_numpy().ravel()

            models[i][0].fit(X_train, y_train)

        y_test_pred = models[i][0].predict(X_test)

        rmse, mae, r2 = evaluate_model(y_test, y_test_pred, toggle_print=True, labels=labels)

        metrics = {
            "rmse": rmse[0],
            "mae": mae[0],
            "r2": r2[0],
        }

        # Saving model & creating meta data
        if models[i][1] == "Random Forest":
            name = f"aqi_{models[i][2]}_day_{i + 1}"
            model_path = str(MODEL_DIR / f"{name}.joblib")
            joblib.dump(models[i][0], model_path)

            model_meta = mr.sklearn.create_model(
                name=name,
                metrics=metrics,
                description=f"AQI Day {i + 1} Predictor"
            )
        elif models[i][1] == "XGBoost":
            name = f"aqi_{models[i][2]}_day_{i + 1}"
            model_path = str(MODEL_DIR / f"{name}.json")
            models[i][0].save_model(model_path)

            model_meta = mr.python.create_model(
                name=name,
                metrics=metrics,
                description=f"AQI Day {i + 1} Predictor"
            )
        elif models[i][1] == "LightGBM":
            name = f"aqi_{models[i][2]}_day_{i + 1}"
            model_path = str(MODEL_DIR / f"{name}.txt")
            models[i][0].booster_.save_model(model_path)

            model_meta = mr.python.create_model(
                name=name,
                metrics=metrics,
                description=f"AQI Day {i + 1} Predictor"
            )
        elif models[i][1] == "MLP":
            name = f"aqi_{models[i][2]}_day_{i + 1}"
            model_path = str(MODEL_DIR / f"{name}.keras")
            models[i][0].save(model_path)

            model_meta = mr.tensorflow.create_model(
                name=name,
                metrics=metrics,
                description=f"AQI Day {i + 1} Predictor"
            )

        # Saving to model registry
        model_meta.save(model_path)

    scaler_path = MODEL_DIR / "scaler.joblib"

    joblib.dump(scaler, scaler_path)

    scaler_meta = mr.sklearn.create_model(
        name="aqi_preprocessor",
        description=f"AQI models robust scaler preprocessor."
    )

    scaler_meta.save(str(scaler_path))