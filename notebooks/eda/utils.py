import pandas as pd
import matplotlib.pyplot as plt

from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import RFECV
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import PredefinedSplit

from src.common.constants import TARGET_COLUMNS


def create_eda_model() -> RandomForestRegressor:
    """
        Create random forest model for eda.

        :return: None
    """

    baseline_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )

    return baseline_model

def calculate_feature_target_correlations(train_df: DataFrame, features: list[str]) -> DataFrame:
    """
        Gives feature correlation.

        :param train_df: Training data frame
        :param features: All features names
        :return: Correlation Dataframe
    """
    corr = (
        train_df[features]
        .corr()
        .abs()
    )

    return corr

def select_features_with_rfecv(input_features: list[str], train_df: DataFrame, val_df: DataFrame) -> None:
    """
        Gives RFECV for the features.

        :param input_features: All input features names
        :param train_df: Training data frame
        :param val_df: Validation data frame
        :return: None
    """

    def rfecv_score(estimator, X, y):
        predictions = estimator.predict(X)
        return -root_mean_squared_error(y, predictions)

    split = [-1] * len(train_df) + [0] * len(val_df)

    X_full = pd.concat(
        [
            train_df[input_features],
            val_df[input_features],
        ],
        ignore_index=True,
    )

    y_full = pd.concat(
        [
            train_df[TARGET_COLUMNS],
            val_df[TARGET_COLUMNS],
        ],
        ignore_index=True,
    )

    cv = PredefinedSplit(test_fold=split)

    rfecv_model = create_eda_model()

    rfecv = RFECV(
        estimator=rfecv_model,
        step=1,
        cv=cv,
        scoring=rfecv_score,
        n_jobs=-1,
    )

    rfecv.fit(X_full, y_full)

    RFECV_FEATURES = X_full.columns[rfecv.support_].tolist()

    print("Selected features:")
    for feature in RFECV_FEATURES:
        print(feature)

    print(f"\nSelected feature count: {len(RFECV_FEATURES)}")

    plt.figure(figsize=(8, 5))

    plt.plot(
        range(1, len(rfecv.cv_results_["mean_test_score"]) + 1),
        rfecv.cv_results_["mean_test_score"],
        marker="o",
    )

    plt.xlabel("Number of Features")
    plt.ylabel("Validation Score (Negative RMSE)")
    plt.title("RFECV Feature Selection")
    plt.tight_layout()
    plt.show()