import numpy as np
from keras import Sequential
from pandas import DataFrame
from sklearn.preprocessing import RobustScaler

from src.common.constants import ALL_LOG_TRANSFORM_FEATURES, ALL_TRAINING_FEATURES, SELECTED_FEATURES_LIST, \
    LATEST_SELECTED_FEATURES_LIST


def get_prediction(df: DataFrame, models: list[tuple[Sequential, str]], scaler: RobustScaler) -> list[np.ndarray]:
    """
        Get predictions

        :param df: Dataframe containing the required data
        :param models: List of models
        :param scaler: Fitted robust scaler
        :return: List of predictions
    """
    df_preprocess = df.copy()

    # Apply log1p on highly skewed features
    for feature in ALL_LOG_TRANSFORM_FEATURES:
        df_preprocess[feature] = np.log1p(df_preprocess[feature])

    # Robust scaling on all features
    df_preprocess[ALL_TRAINING_FEATURES] = scaler.transform(
        df_preprocess[ALL_TRAINING_FEATURES]
    )

    predictions = []

    for i, feature_list in enumerate(LATEST_SELECTED_FEATURES_LIST):
        if models[i][1] == "MLP":
            prediction = models[i][0].predict(df_preprocess[feature_list])
        else:
            prediction = models[i][0].predict(df[feature_list])

        predictions.append(prediction)

    return predictions