from keras import Sequential, Input
from keras.src.layers import Dense, Dropout
from keras.src.optimizers import Adam
from pandas import DataFrame
from sklearn.preprocessing import RobustScaler
from tensorflow.python.keras.regularizers import l2


def build_mlp_model(total_features: int) -> Sequential:
    """
        Build a fresh mlp model.

        :param total_features: Number of total features
        :return: Mlp model
    """
    mlp_model = Sequential([
        Input(shape=(total_features,)),
        Dense(
            128,
            activation="relu",
            kernel_regularizer=l2(1e-3),
        ),
        Dropout(0.15),
        Dense(1, activation="linear"),
    ])

    mlp_model.compile(
        optimizer=Adam(learning_rate=5e-3),
        loss="huber",
    )

    return mlp_model

def fit_robust_scaler(train_df: DataFrame, features: list[str]) -> RobustScaler:
    """
        Fit and return robust scaler

        :param train_df: Training dataframe
        :param features: List of features on which to perform
        :return: Robust scaler
    """
    
    scaler = RobustScaler()

    train_df[features] = scaler.fit_transform(
        train_df[features]
    )

    return scaler
