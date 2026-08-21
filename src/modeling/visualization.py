import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame

from src.common.constants import TARGET_COLUMNS


def plot_actual_vs_predicted(y_val: DataFrame, y_val_pred: np.ndarray) -> None:
    """
        Plot actual vs predicted graph.

        :param y_val: Validation labels
        :param y_val_pred: Model's predictions
        :return: None
    """

    for i, target in enumerate(TARGET_COLUMNS):
        plt.figure(figsize=(7, 6))

        plt.scatter(y_val.iloc[:, i], y_val_pred[:, i], alpha=0.6)

        min_value = min(y_val.iloc[:, i].min(), y_val_pred[:, i].min())
        max_value = max(y_val.iloc[:, i].max(), y_val_pred[:, i].max())

        plt.plot(
            [min_value, max_value],
            [min_value, max_value],
            linestyle="--"
        )

        plt.xlabel("Actual AQI")
        plt.ylabel("Predicted AQI")
        plt.title(f"Actual vs Predicted — {target}")
        plt.tight_layout()
        plt.show()