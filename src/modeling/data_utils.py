import numpy as np
import pandas as pd
from pandas import DataFrame
from IPython.display import display
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

from notebooks.eda.utils import create_eda_model
from src.common.constants import BASELINE_FEATURES, TARGET_COLUMNS
from src.modeling.visualization import plot_actual_vs_predicted

type MetricResults = tuple[np.ndarray, np.ndarray, np.ndarray]

type ModelMetrics = tuple[str, MetricResults]


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
                             baseline: list[str] | None  = None) -> tuple[RandomForestRegressor, MetricResults]:
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
        :return: None
    """

    X_train, y_train, X_val, y_val = prepare_features_and_targets(train_df, val_df, additonal_features, baseline = baseline)

    model = create_eda_model()

    model.fit(X_train, y_train)

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