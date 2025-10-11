"""Dataset registry for the Jarvis AI project.

Each dataset entry encapsulates metadata required by the analysis and
modeling pipelines. The datasets are synthetic representations inspired by
those listed in the project instructions. They are generated with the helper
script located at :mod:`scripts.generate_synthetic_datasets`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class TaskType(str, Enum):
    """High level task taxonomy used to select the modelling strategy."""

    REGRESSION = "regression"
    CLASSIFICATION = "classification"
    TIME_SERIES = "time_series"
    RECOMMENDATION = "recommendation"


@dataclass(frozen=True)
class DatasetInfo:
    """Metadata describing a dataset used in the project."""

    name: str
    filename: str
    task: TaskType
    target: str | None
    description: str
    features: List[str]
    time_column: str | None = None
    group_keys: List[str] | None = None

    @property
    def path(self) -> Path:
        return DATA_DIR / self.filename


_DATASETS: Dict[str, DatasetInfo] = {
    "bitcoin_price": DatasetInfo(
        name="Predicción del precio de Bitcoin",
        filename="bitcoin_prices.csv",
        task=TaskType.TIME_SERIES,
        target="close",
        description="Serie temporal sintética que simula precios diarios de Bitcoin.",
        features=["open", "high", "low", "close", "volume"],
        time_column="date",
    ),
    "car_price": DatasetInfo(
        name="Predicción del precio de un automóvil",
        filename="car_prices.csv",
        task=TaskType.REGRESSION,
        target="selling_price",
        description="Datos estructurados sobre vehículos usados con atributos técnicos y de mercado.",
        features=[
            "year",
            "present_price",
            "kms_driven",
            "fuel_type",
            "seller_type",
            "transmission",
            "owner",
        ],
    ),
    "movie_recs": DatasetInfo(
        name="Recomendación de películas",
        filename="movie_ratings.csv",
        task=TaskType.RECOMMENDATION,
        target="rating",
        description="Calificaciones usuario-película para alimentar un sistema de recomendación.",
        features=["user_id", "movie_id", "rating"],
    ),
    "sp500_price": DatasetInfo(
        name="Predicción de precios S&P 500",
        filename="sp500_prices.csv",
        task=TaskType.TIME_SERIES,
        target="close",
        description="Cotizaciones sintéticas para múltiples símbolos del índice S&P 500.",
        features=["open", "high", "low", "close", "volume"],
        time_column="date",
        group_keys=["symbol"],
    ),
    "house_price": DatasetInfo(
        name="Predicción de precios de vivienda",
        filename="house_prices.csv",
        task=TaskType.REGRESSION,
        target="sale_price",
        description="Variables estructurales de viviendas y su precio de venta.",
        features=[
            "lot_area",
            "overall_qual",
            "year_built",
            "gr_liv_area",
            "garage_cars",
            "neighborhood",
            "house_style",
        ],
    ),
    "wine_quality": DatasetInfo(
        name="Clasificación de calidad del vino",
        filename="wine_quality.csv",
        task=TaskType.CLASSIFICATION,
        target="quality",
        description="Métricas fisicoquímicas de vinos con etiquetas de calidad.",
        features=[
            "fixed_acidity",
            "volatile_acidity",
            "citric_acid",
            "residual_sugar",
            "chlorides",
            "free_sulfur_dioxide",
            "total_sulfur_dioxide",
            "density",
            "pH",
            "sulphates",
            "alcohol",
        ],
    ),
    "inventory_demand": DatasetInfo(
        name="Predicción de inventario",
        filename="inventory_demand.csv",
        task=TaskType.TIME_SERIES,
        target="units_sold",
        description="Histórico de ventas por tienda y artículo para planificación de inventario.",
        features=["store", "item", "units_sold"],
        time_column="date",
        group_keys=["store", "item"],
    ),
    "bike_fare": DatasetInfo(
        name="Tarifa de viajes en bicicleta",
        filename="bike_fares.csv",
        task=TaskType.REGRESSION,
        target="fare",
        description="Características de viajes compartidos de bicicleta con tarifa final.",
        features=["distance_km", "duration_min", "surge_multiplier", "city"],
    ),
    "telco_churn": DatasetInfo(
        name="Churn de clientes Telco",
        filename="telco_churn.csv",
        task=TaskType.CLASSIFICATION,
        target="Churn",
        description="Información contractual y de uso de clientes de telecomunicaciones.",
        features=[
            "gender",
            "SeniorCitizen",
            "Partner",
            "Dependents",
            "tenure",
            "PhoneService",
            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "Contract",
            "PaperlessBilling",
            "PaymentMethod",
            "MonthlyCharges",
            "TotalCharges",
        ],
    ),
    "airline_delay": DatasetInfo(
        name="Retrasos en vuelos",
        filename="airline_delays.csv",
        task=TaskType.CLASSIFICATION,
        target="cancelled",
        description="Registros de vuelos con información de demoras y cancelaciones.",
        features=[
            "airline",
            "origin",
            "destination",
            "distance",
            "weather",
            "departure_delay",
            "arrival_delay",
        ],
    ),
}


def get_dataset(key: str) -> DatasetInfo:
    try:
        return _DATASETS[key]
    except KeyError as exc:  # pragma: no cover - defensive clause
        raise KeyError(f"Dataset '{key}' is not registered") from exc


def iter_datasets() -> Iterable[DatasetInfo]:
    return _DATASETS.values()
