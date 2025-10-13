"""Dataset registry for the Jarvis AI project."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, Iterable, List

import pandas as pd

from . import data_loading

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


class TaskType(str, Enum):
    """High level task taxonomy used to select the modelling strategy."""

    REGRESSION = "regression"
    CLASSIFICATION = "classification"
    TIME_SERIES = "time_series"


Loader = Callable[[Path], pd.DataFrame]


@dataclass(frozen=True)
class DatasetInfo:
    """Metadata describing a dataset used in the project."""

    name: str
    filename: str
    task: TaskType
    target: str
    description: str
    features: List[str] | None = None
    time_column: str | None = None
    group_keys: List[str] | None = None
    loader: Loader | None = None

    @property
    def path(self) -> Path:
        return DATA_DIR / self.filename

    def load_dataframe(self) -> pd.DataFrame:
        if self.loader is not None:
            return self.loader(self.path)
        return pd.read_csv(self.path)


_DATASETS: Dict[str, DatasetInfo] = {
    "bitcoin_price": DatasetInfo(
        name="Precio histórico de Bitcoin",
        filename="bitcoin_price_training.csv",
        task=TaskType.TIME_SERIES,
        target="close",
        description="Cotizaciones diarias de Bitcoin con valores OHLC y capitalización.",
        time_column="date",
        loader=data_loading.load_bitcoin_prices,
    ),
    "avocado_prices": DatasetInfo(
        name="Precios de aguacate por región",
        filename="avocado.csv",
        task=TaskType.REGRESSION,
        target="average_price",
        description="Ventas de aguacate en Estados Unidos segmentadas por región y tipo.",
        loader=data_loading.load_avocado,
    ),
    "body_fat": DatasetInfo(
        name="Porcentaje de grasa corporal",
        filename="bodyfat.csv",
        task=TaskType.REGRESSION,
        target="body_fat",
        description="Mediciones antropométricas para estimar el porcentaje de grasa.",
        loader=data_loading.load_bodyfat,
    ),
    "car_prices": DatasetInfo(
        name="Valor de automóviles usados",
        filename="car_prices.csv",
        task=TaskType.REGRESSION,
        target="selling_price",
        description="Histórico de vehículos usados con características de mercado.",
        loader=data_loading.load_car_prices,
    ),
    "telco_churn": DatasetInfo(
        name="Churn de clientes Telco",
        filename="telco_churn.csv",
        task=TaskType.CLASSIFICATION,
        target="churn",
        description="Información contractual y de uso de clientes de telecomunicaciones.",
        loader=data_loading.load_telco_churn,
    ),
    "wine_quality": DatasetInfo(
        name="Calidad de vinos",
        filename="winequality.csv",
        task=TaskType.CLASSIFICATION,
        target="quality",
        description="Mediciones fisicoquímicas de vinos blancos y tintos.",
        loader=data_loading.load_wine_quality,
    ),
    "stroke_risk": DatasetInfo(
        name="Predicción de derrame cerebral",
        filename="healthcare_stroke_data.csv",
        task=TaskType.CLASSIFICATION,
        target="stroke",
        description="Variables demográficas y clínicas asociadas al derrame cerebral.",
        loader=data_loading.load_stroke_data,
    ),
    "hepatitis_c": DatasetInfo(
        name="Diagnóstico de hepatitis C",
        filename="hepatitis_c_data.csv",
        task=TaskType.CLASSIFICATION,
        target="category",
        description="Perfil bioquímico con etiquetado diagnóstico para hepatitis C.",
        loader=data_loading.load_hepatitis_c,
    ),
    "cirrhosis_status": DatasetInfo(
        name="Estatus clínico de cirrosis",
        filename="cirrhosis.csv",
        task=TaskType.CLASSIFICATION,
        target="status",
        description="Datos longitudinales de pacientes con cirrosis hepática.",
        loader=data_loading.load_cirrhosis,
    ),
}


def get_dataset(key: str) -> DatasetInfo:
    try:
        return _DATASETS[key]
    except KeyError as exc:  # pragma: no cover - defensive clause
        raise KeyError(f"Dataset '{key}' is not registered") from exc


def iter_datasets() -> Iterable[DatasetInfo]:
    return _DATASETS.values()
