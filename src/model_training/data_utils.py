from keras import Sequential, Input
from keras.src.layers import Dense, Dropout
from keras.src.optimizers import Adam
from lightgbm import LGBMRegressor
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import RobustScaler
from tensorflow.python.keras.regularizers import l2
from xgboost import XGBRegressor

from src.common.constants import LATEST_SELECTED_FEATURES_TARGET_2


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

def get_day_1_model() -> XGBRegressor:
    """
        Give day 1 model

        :return: XGB Regressor
    """
    return XGBRegressor(
        subsample=0.6,
        reg_lambda=1.0,
        reg_alpha=0.1,
        n_estimators=500,
        min_child_weight=1,
        max_depth=None,
        learning_rate=0.01,
        colsample_bytree=0.6,
        random_state=42,
        n_jobs=-1,
    )

def get_day_2_model() -> Sequential:
    """
        Give day 2 model

        :return: Sequential Model
    """

    input_dim = len(LATEST_SELECTED_FEATURES_TARGET_2)
    model = Sequential(
        [
            Input(shape=(input_dim,)),
            Dense(
                64,
                activation="relu",
                kernel_regularizer=l2(1e-4),
            ),
            Dropout(0.1),
            Dense(
                32,
                activation="relu",
                kernel_regularizer=l2(1e-4),
            ),
            Dropout(0.1),
            Dense(1, activation="linear"),
        ]
    )

    model.compile(
        optimizer=Adam(
            learning_rate=1e-3
        ),
        loss="mse",
    )

    return model

def get_day_3_model() -> LGBMRegressor:
    """
        Give day 3 model

        :return: LGBM Regressor
    """

    return LGBMRegressor(
        subsample=0.6,
        reg_lambda=10.0,
        reg_alpha=0,
        num_leaves=75,
        n_estimators=100,
        min_child_samples=50,
        max_depth=3,
        learning_rate=0.05,
        colsample_bytree=1.0,
        random_state=42,
        n_jobs=-1,
        verbosity=-1,
    )

def get_day_4_model() -> RandomForestRegressor:
    """
        Give day 3 model

        :return: LGBM Regressor
    """

    return RandomForestRegressor(
        n_estimators=100,
        min_samples_split=5,
        min_samples_leaf=8,
        max_features=1.0,
        max_depth=20,
        random_state=42,
        n_jobs=-1,
    )
