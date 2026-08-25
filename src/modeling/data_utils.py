from typing import Any

import numpy as np
import pandas as pd
from keras.src.callbacks import EarlyStopping
from pandas import DataFrame
from pathlib import Path
from IPython.display import display
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import RobustScaler

from notebooks.eda.utils import create_eda_model
from src.common.constants import BASELINE_FEATURES, TARGET_COLUMNS, LOG_TRANSFORM_FEATURES, FINAL_SELECTED_FEATURES
from src.common.schemas import DeepLearningFitParamSchema
from src.modeling.visualization import plot_actual_vs_predicted


type MetricResults = tuple[np.ndarray, np.ndarray, np.ndarray]

type ModelMetrics = tuple[str, MetricResults]

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def prepare_features_and_targets(train_df: DataFrame, val_df: DataFrame, additional_features: list[str] | None = None,
                                 baseline: list[str] | None = None) \
        -> tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    """
        Prepare features and targets for training

        :param train_df: Training dataframe
        :param val_df: Validation dataframe
        :param additional_features: Optional additional features
        :param baseline: Optional baseline to replace Baseline constant
        :return: Train and validation features and targets
    """

    if baseline:
        features = baseline
    else:
        features = BASELINE_FEATURES

    if additional_features is not None:
        features = features + additional_features

    X_train = train_df[features]
    y_train = train_df[TARGET_COLUMNS]

    X_val = val_df[features]
    y_val = val_df[TARGET_COLUMNS]

    return X_train, y_train, X_val, y_val

def evaluate_model(y_val: DataFrame, y_val_pred: np.ndarray, toggle_print: bool = False) -> MetricResults:
    """
        Evaluate RMSE, MAE, R2 metrics for the model.

        :param y_val: Validation labels
        :param y_val_pred: Model's predictions
        :param toggle_print: A toggle for print
        :return: The metrics
    """

    rmse = root_mean_squared_error(y_val, y_val_pred, multioutput="raw_values")
    mae = mean_absolute_error(y_val, y_val_pred, multioutput="raw_values")
    r2 = r2_score(y_val, y_val_pred, multioutput="raw_values")

    if toggle_print:
        for i, target in enumerate(TARGET_COLUMNS):
            print(f"\n{target}")
            print(f"  RMSE: {rmse[i]:.4f}")
            print(f"  MAE:  {mae[i]:.4f}")
            print(f"  R²:   {r2[i]:.4f}")

    return rmse, mae, r2

def compare_model_metrics(model_1: ModelMetrics, model_2: ModelMetrics) -> None:
    """
        Compare metrics from two models in a side-by-side table.

        :param model_1: Tuple containing the model label and its metrics.
        :param model_2: Tuple containing the model label and its metrics.
        :return: None
    """

    model_1_label, (rmse_1, mae_1, r2_1) = model_1
    model_2_label, (rmse_2, mae_2, r2_2) = model_2

    rows = []

    for i, target in enumerate(TARGET_COLUMNS):
        rows.append({
            "Target": target,
            f"{model_1_label} RMSE": rmse_1[i],
            f"{model_1_label} MAE": mae_1[i],
            f"{model_1_label} R²": r2_1[i],
            f"{model_2_label} RMSE": rmse_2[i],
            f"{model_2_label} MAE": mae_2[i],
            f"{model_2_label} R²": r2_2[i],
        })

    rows.append({
        "Target": "Mean",
        f"{model_1_label} RMSE": rmse_1.mean(),
        f"{model_1_label} MAE": mae_1.mean(),
        f"{model_1_label} R²": r2_1.mean(),
        f"{model_2_label} RMSE": rmse_2.mean(),
        f"{model_2_label} MAE": mae_2.mean(),
        f"{model_2_label} R²": r2_2.mean(),
    })

    display(pd.DataFrame(rows))

def train_and_evaluate_model(train_df: DataFrame, val_df: DataFrame, label: str | None = None,
                             additonal_features: list[str] | None = None, compare_model: ModelMetrics | None = None,
                             toggle_evaluate_print: bool = False, disable_plot: bool = False,
                             baseline: list[str] | None  = None, model: Any = None,
                             deep_learning: DeepLearningFitParamSchema | bool = False) \
        -> tuple[RandomForestRegressor, MetricResults]:
    """
        Train and Evaluate model

        :param train_df: Train data frame
        :param val_df: Validation data frame
        :param label: Label of the model
        :param additonal_features: Additional features' names
        :param compare_model: Another model's label and metrics for comparison
        :param toggle_evaluate_print: Toggle evaluate_model's prints
        :param disable_plot: Toggle for plot
        :param baseline: Optional baseline to replace Baseline constant
        :param model: Optional model
        :param deep_learning: Optional deep learning toggle
        :return: None
    """

    X_train, y_train, X_val, y_val = prepare_features_and_targets(train_df, val_df, additonal_features, baseline = baseline)

    if model is None:
        model = create_eda_model()

    if deep_learning is False:
        model.fit(X_train, y_train)
    else:
        model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val),
            **deep_learning
        )

    y_val_pred = model.predict(X_val)

    rmse, mae, r2 = evaluate_model(y_val, y_val_pred, toggle_print = toggle_evaluate_print)

    if compare_model is not None and label is not None:
        compare_model_metrics(
            compare_model,
            (label, (rmse, mae, r2))
        )

    if not disable_plot:
        plot_actual_vs_predicted(y_val, y_val_pred)

    return model, (rmse, mae, r2)

def load_modeling_data() -> DataFrame:
    """
    Load model data.

    :return: DataFrame
    """
    data_path = PROJECT_ROOT / "notebooks" / "eda" / "data" / "engineered_features.parquet"

    df = pd.read_parquet(data_path)

    df = (
        df.dropna(subset=TARGET_COLUMNS)
        .sort_values("ts")
        .reset_index(drop=True)
    )

    return df

def split_modeling_data(df: DataFrame) -> tuple[DataFrame, DataFrame, DataFrame]:
    """
        Splitting data for models

        :param df: The full dataframe.
        :return: Return train, val, and test splits
    """

    train_end = int(len(df) * 0.70)
    val_end = int(len(df) * 0.85)

    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()

    return train_df, val_df, test_df

def apply_log_transform(
    train_df: DataFrame,
    val_df: DataFrame,
    test_df: DataFrame,
) -> tuple[DataFrame, DataFrame, DataFrame]:
    """
        Apply log transform on highly skewed features.

        :param train_df: Training dataframe
        :param val_df: Validating dataframe
        :param test_df: Testing dataframe
        :return: Return log applied train, val, and test dataframes
    """

    features = LOG_TRANSFORM_FEATURES

    train_df = train_df.copy()
    val_df = val_df.copy()
    test_df = test_df.copy()

    for feature in features:
        train_df[feature] = np.log1p(train_df[feature])
        val_df[feature] = np.log1p(val_df[feature])
        test_df[feature] = np.log1p(test_df[feature])

    return train_df, val_df, test_df

def apply_robust_scaler(
    train_df: DataFrame,
    val_df: DataFrame,
    test_df: DataFrame,
) -> tuple[DataFrame, DataFrame, DataFrame]:
    """
        Apply robust scaler on the dataframes.

        :param train_df: Training dataframe
        :param val_df: Validating dataframe
        :param test_df: Testing dataframe
        :return: Return robust scaled train, val, and test dataframes
    """

    train_df = train_df.copy()
    val_df = val_df.copy()
    test_df = test_df.copy()

    scaler = RobustScaler()

    train_df[FINAL_SELECTED_FEATURES] = scaler.fit_transform(
        train_df[FINAL_SELECTED_FEATURES]
    )

    val_df[FINAL_SELECTED_FEATURES] = scaler.transform(
        val_df[FINAL_SELECTED_FEATURES]
    )

    test_df[FINAL_SELECTED_FEATURES] = scaler.transform(
        test_df[FINAL_SELECTED_FEATURES]
    )

    return train_df, val_df, test_df

def preprocess_data(
    train_df: DataFrame,
    val_df: DataFrame,
    test_df: DataFrame,
) -> tuple[DataFrame, DataFrame, DataFrame]:
    """
        Apply both log and robust scaler on the dataframes.

        :param train_df: Training dataframe
        :param val_df: Validating dataframe
        :param test_df: Testing dataframe
        :return: Return preprocessed train, val, and test dataframes
    """

    train_df = train_df.copy()
    val_df = val_df.copy()
    test_df = test_df.copy()

    train_df, val_df, test_df = apply_log_transform(train_df, val_df, test_df)

    train_df, val_df, test_df = apply_robust_scaler(train_df, val_df, test_df)

    return train_df, val_df, test_df

