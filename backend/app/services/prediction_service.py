import numpy as np
from keras import Sequential
from pandas import DataFrame
from sklearn.preprocessing import RobustScaler

from src.common.constants import ALL_LOG_TRANSFORM_FEATURES, ALL_TRAINING_FEATURES, SELECTED_FEATURES_LIST


def get_prediction(df: DataFrame, models: list[Sequential], scaler: RobustScaler) -> list[np.ndarray]:
    """
        Get predictions

        :param df: Dataframe containing the required data
        :param models: List of models
        :param scaler: Fitted robust scaler
        :return: List of predictions
    """

    # Apply log1p on highly skewed features
    for feature in ALL_LOG_TRANSFORM_FEATURES:
        df[feature] = np.log1p(df[feature])

    # Robust scaling on all features
    df[ALL_TRAINING_FEATURES] = scaler.transform(
        df[ALL_TRAINING_FEATURES]
    )

    predictions = []

    for i, feature_list in enumerate(SELECTED_FEATURES_LIST):
        prediction = models[i].predict(df[feature_list])

        predictions.append(prediction)

    return predictions