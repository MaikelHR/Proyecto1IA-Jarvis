"""Model training utilities for the Jarvis IA project."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from .dataset_registry import DatasetInfo, TaskType

REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)


@dataclass
class ModelResult:
    dataset: str
    task: TaskType
    metrics: Dict[str, float]
    model_path: Path | None = None

    def to_dict(self) -> Dict[str, object]:
        data: Dict[str, object] = {
            "dataset": self.dataset,
            "task": self.task.value,
            "metrics": self.metrics,
        }
        if self.model_path is not None:
            data["model_path"] = str(self.model_path)
        return data


def _split_xy(df: pd.DataFrame, dataset_info: DatasetInfo) -> Tuple[pd.DataFrame, pd.Series]:
    if dataset_info.target is None:
        raise ValueError(f"Dataset {dataset_info.name} does not define a target column")
    y = df[dataset_info.target]
    X = df.drop(columns=[dataset_info.target])
    return X, y


def _regression_pipeline(X: pd.DataFrame) -> ColumnTransformer:
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    transformers = []
    if numeric_features:
        transformers.append(("num", numeric_transformer, numeric_features))
    if categorical_features:
        transformers.append(("cat", categorical_transformer, categorical_features))
    if not transformers:
        raise ValueError("No features available for modelling")
    return ColumnTransformer(transformers)


def _evaluate_regression(y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    denominator = float(np.sum((y_true - y_true.mean()) ** 2))
    if denominator == 0:
        r2 = float("nan")
    else:
        r2 = float(1 - np.sum((y_true - y_pred) ** 2) / denominator)
    return {"rmse": rmse, "mae": mae, "r2": r2}


def _evaluate_classification(y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
    binary = y_true.nunique() == 2
    average = "binary" if binary else "weighted"
    pos_label = None
    if binary:
        pos_label = sorted(y_true.unique())[-1]
    metric_kwargs = {"average": average, "zero_division": 0}
    if pos_label is not None:
        metric_kwargs["pos_label"] = pos_label
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, **metric_kwargs)),
        "recall": float(recall_score(y_true, y_pred, **metric_kwargs)),
        "f1": float(f1_score(y_true, y_pred, **metric_kwargs)),
    }


def _evaluate_time_series(y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    mape = float(np.mean(np.abs((y_true - y_pred) / np.clip(np.abs(y_true), 1e-6, None))))
    return {"rmse": rmse, "mae": mae, "mape": mape}


def _prepare_time_series_features(df: pd.DataFrame, dataset_info: DatasetInfo) -> Tuple[pd.DataFrame, pd.Series]:
    if dataset_info.time_column is None:
        raise ValueError("Time series dataset requires a time column")

    df = df.copy()
    df[dataset_info.time_column] = pd.to_datetime(df[dataset_info.time_column])
    grouping = dataset_info.group_keys or []
    df = df.sort_values((grouping or []) + [dataset_info.time_column])

    feature_cols = [col for col in dataset_info.features if col != dataset_info.target]
    grouped = df.groupby(grouping) if grouping else [(None, df)]
    for _, group_df in grouped:
        idx = group_df.index
        df.loc[idx, "lag_1"] = group_df[dataset_info.target].shift(1)
        df.loc[idx, "lag_7"] = group_df[dataset_info.target].shift(7)
        df.loc[idx, "rolling_mean_7"] = group_df[dataset_info.target].rolling(window=7, min_periods=1).mean()
    df = df.dropna(subset=["lag_1", "lag_7"])

    extra_features = ["lag_1", "lag_7", "rolling_mean_7"]
    X = df[feature_cols + extra_features].drop(columns=[dataset_info.time_column], errors="ignore")
    y = df[dataset_info.target]
    return X, y


def _prepare_recommendation(df: pd.DataFrame, dataset_info: DatasetInfo) -> Tuple[pd.DataFrame, pd.Series]:
    required_cols = {"user_id", "movie_id", dataset_info.target}
    if not required_cols.issubset(df.columns):
        raise ValueError("Movie recommendation dataset must contain user_id and movie_id columns")
    return df[["user_id", "movie_id"]], df[dataset_info.target]


def train_dataset(dataset_info: DatasetInfo) -> ModelResult:
    df = pd.read_csv(dataset_info.path)

    if dataset_info.task == TaskType.REGRESSION:
        X, y = _split_xy(df, dataset_info)
        preprocessor = _regression_pipeline(X)
        model = GradientBoostingRegressor(random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
        )
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        metrics = _evaluate_regression(y_test, y_pred)
        path = REPORT_DIR / f"{dataset_info.path.stem}_model.pkl"
        pd.to_pickle(pipeline, path)
        return ModelResult(dataset=dataset_info.name, task=dataset_info.task, metrics=metrics, model_path=path)

    if dataset_info.task == TaskType.CLASSIFICATION:
        X, y = _split_xy(df, dataset_info)
        preprocessor = _regression_pipeline(X)
        model = LogisticRegression(max_iter=500)
        stratify = y if y.nunique() > 1 else None
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=stratify,
        )
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        metrics = _evaluate_classification(y_test, y_pred)
        path = REPORT_DIR / f"{dataset_info.path.stem}_model.pkl"
        pd.to_pickle(pipeline, path)
        return ModelResult(dataset=dataset_info.name, task=dataset_info.task, metrics=metrics, model_path=path)

    if dataset_info.task == TaskType.TIME_SERIES:
        X, y = _prepare_time_series_features(df, dataset_info)
        preprocessor = _regression_pipeline(X)
        model = GradientBoostingRegressor(random_state=42)
        split_index = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
        y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        metrics = _evaluate_time_series(y_test, y_pred)
        path = REPORT_DIR / f"{dataset_info.path.stem}_model.pkl"
        pd.to_pickle(pipeline, path)
        return ModelResult(dataset=dataset_info.name, task=dataset_info.task, metrics=metrics, model_path=path)

    if dataset_info.task == TaskType.RECOMMENDATION:
        features, ratings = _prepare_recommendation(df, dataset_info)
        frame = pd.concat([features, ratings.rename("rating")], axis=1)
        frame = frame.sample(frac=1.0, random_state=42).reset_index(drop=True)
        split_index = int(len(frame) * 0.8)
        train_df, test_df = frame.iloc[:split_index], frame.iloc[split_index:]
        global_mean = train_df["rating"].mean()
        user_means = train_df.groupby("user_id")["rating"].mean().to_dict()
        movie_means = train_df.groupby("movie_id")["rating"].mean().to_dict()

        def _predict(row: pd.Series) -> float:
            user_bias = user_means.get(row["user_id"], global_mean) - global_mean
            movie_bias = movie_means.get(row["movie_id"], global_mean) - global_mean
            return global_mean + user_bias + movie_bias

        y_true = test_df["rating"]
        y_pred = test_df.apply(_predict, axis=1)
        rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
        mae = float(mean_absolute_error(y_true, y_pred))
        metrics = {"rmse": rmse, "mae": mae}
        bias_model = {
            "global_mean": global_mean,
            "user_means": user_means,
            "movie_means": movie_means,
        }
        path = REPORT_DIR / f"{dataset_info.path.stem}_recommender.pkl"
        pd.to_pickle(bias_model, path)
        return ModelResult(dataset=dataset_info.name, task=dataset_info.task, metrics=metrics, model_path=path)

    raise ValueError(f"Unsupported task type: {dataset_info.task}")


def save_model_result(result: ModelResult) -> Path:
    path = REPORT_DIR / f"{result.dataset.lower().replace(' ', '_')}_metrics.json"
    pd.Series(result.to_dict()).to_json(path, indent=2, force_ascii=False)
    return path
