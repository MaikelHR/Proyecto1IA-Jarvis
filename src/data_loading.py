"""Dataset loading and cleaning utilities."""

from __future__ import annotations

import re
from pathlib import Path
import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def _normalize_column_name(name: str) -> str:
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", str(name))
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    name = name.strip("_").lower()
    if not name:
        name = "column"
    if name[0].isdigit():
        name = f"col_{name}"
    return name


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = []
    seen: dict[str, int] = {}
    for column in df.columns:
        base = _normalize_column_name(column)
        count = seen.get(base, 0)
        if count:
            new_name = f"{base}_{count+1}"
        else:
            new_name = base
        seen[base] = count + 1
        renamed.append(new_name)
    df = df.copy()
    df.columns = renamed
    return df


def _drop_unnamed(df: pd.DataFrame) -> pd.DataFrame:
    mask = [not str(col).lower().startswith("unnamed") for col in df.columns]
    return df.loc[:, mask]


def load_avocado(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    df = _drop_unnamed(df)
    df = _normalize_columns(df)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.dropna(subset=["average_price"])


def load_bitcoin_prices(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    df = _drop_unnamed(df)
    df = _normalize_columns(df)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric_cols = [col for col in df.columns if col != "date"]
    for col in numeric_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["close"])
    return df.reset_index(drop=True)


def load_bodyfat(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    df = _normalize_columns(df)
    return df.dropna(subset=["body_fat"])


def load_car_prices(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    df = _normalize_columns(df)
    return df.dropna(subset=["selling_price"])


def load_telco_churn(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    df = _normalize_columns(df)
    df = df.drop(columns=["customerid"], errors="ignore")
    if "total_charges" in df.columns:
        df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
    return df.dropna(subset=["churn"])


def load_wine_quality(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    df = _normalize_columns(df)
    return df.dropna(subset=["quality"])


def load_stroke_data(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    df = _normalize_columns(df)
    df = df.drop(columns=["id"], errors="ignore")
    if "bmi" in df.columns:
        df["bmi"] = pd.to_numeric(df["bmi"], errors="coerce")
    return df.dropna(subset=["stroke"])


def load_hepatitis_c(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    df = _drop_unnamed(df)
    df = _normalize_columns(df)
    if "category" in df.columns:
        df["category"] = (
            df["category"].astype(str).str.split("=").str[-1].str.strip().str.lower()
        )
        df["category"] = df["category"].str.replace(r"[^0-9a-z]+", "_", regex=True)
    return df.dropna(subset=["category"])


def load_cirrhosis(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    df = _normalize_columns(df)
    df = df.drop(columns=["id"], errors="ignore")
    return df.dropna(subset=["status"])


__all__ = [
    "load_avocado",
    "load_bitcoin_prices",
    "load_bodyfat",
    "load_car_prices",
    "load_cirrhosis",
    "load_hepatitis_c",
    "load_stroke_data",
    "load_telco_churn",
    "load_wine_quality",
]
