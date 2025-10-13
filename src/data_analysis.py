"""Exploratory analysis utilities for the Jarvis IA project."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd

from .dataset_registry import DatasetInfo, TaskType

REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)


@dataclass
class ColumnSummary:
    name: str
    dtype: str
    n_missing: int
    example: str | None
    stats: Dict[str, float] | None

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        if self.stats is None:
            data.pop("stats")
        return data


@dataclass
class DatasetSummary:
    dataset: str
    description: str
    task: TaskType
    target: str
    n_rows: int
    n_columns: int
    categorical_columns: List[ColumnSummary]
    numerical_columns: List[ColumnSummary]

    def to_dict(self) -> Dict[str, object]:
        return {
            "dataset": self.dataset,
            "description": self.description,
            "task": self.task.value,
            "target": self.target,
            "n_rows": self.n_rows,
            "n_columns": self.n_columns,
            "categorical_columns": [col.to_dict() for col in self.categorical_columns],
            "numerical_columns": [col.to_dict() for col in self.numerical_columns],
        }


def _summary_for_series(series: pd.Series) -> ColumnSummary:
    is_numeric = pd.api.types.is_numeric_dtype(series)
    n_missing = int(series.isna().sum())
    example = None if series.dropna().empty else str(series.dropna().iloc[0])
    stats: Dict[str, float] | None
    if is_numeric:
        stats = {
            "mean": float(series.mean()),
            "std": float(series.std(ddof=0)),
            "min": float(series.min()),
            "max": float(series.max()),
            "quantiles": {
                "0.25": float(series.quantile(0.25)),
                "0.5": float(series.quantile(0.5)),
                "0.75": float(series.quantile(0.75)),
            },
        }
    else:
        stats = {
            "unique": int(series.nunique()),
            "most_common": None,
        }
        if not series.dropna().empty:
            value_counts = Counter(series.dropna().tolist())
            top_value, top_freq = value_counts.most_common(1)[0]
            stats["most_common"] = {"value": str(top_value), "count": int(top_freq)}
    return ColumnSummary(
        name=series.name,
        dtype=str(series.dtype),
        n_missing=n_missing,
        example=example,
        stats=stats,
    )


def build_summary(df: pd.DataFrame, dataset_info: DatasetInfo) -> DatasetSummary:
    categorical, numerical = [], []
    for column in df.columns:
        summary = _summary_for_series(df[column])
        if pd.api.types.is_numeric_dtype(df[column]):
            numerical.append(summary)
        else:
            categorical.append(summary)
    return DatasetSummary(
        dataset=dataset_info.name,
        description=dataset_info.description,
        task=dataset_info.task,
        target=dataset_info.target,
        n_rows=len(df),
        n_columns=df.shape[1],
        categorical_columns=categorical,
        numerical_columns=numerical,
    )


def save_summary(summary: DatasetSummary, filename: str | None = None) -> Path:
    REPORT_DIR.mkdir(exist_ok=True)
    filename = filename or f"{summary.dataset.lower().replace(' ', '_')}_summary.json"
    path = REPORT_DIR / filename
    pd.Series(summary.to_dict()).to_json(path, force_ascii=False, indent=2)
    return path


def summarize_dataset(dataset_info: DatasetInfo) -> Path:
    df = dataset_info.load_dataframe()
    summary = build_summary(df, dataset_info)
    return save_summary(summary, filename=f"{dataset_info.path.stem}_summary.json")
