"""Utility script to create synthetic datasets used in the project.
The datasets mimic the structure of the datasets described in the project specification
but remain lightweight to keep the repository manageable. The generation is fully
deterministic to ensure reproducibility across runs."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RANDOM_SEED = 42


def _rng() -> np.random.Generator:
    return np.random.default_rng(RANDOM_SEED)


def _save(df: pd.DataFrame, filename: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_DIR / filename, index=False)


def generate_bitcoin_prices(periods: int = 365) -> None:
    rng = _rng()
    dates = pd.date_range("2022-01-01", periods=periods, freq="D")
    returns = rng.normal(0.0008, 0.03, size=periods)
    close = 45000 * (1 + returns).cumprod()
    high = close * (1 + rng.normal(0.01, 0.01, size=periods))
    low = close * (1 - rng.normal(0.01, 0.01, size=periods))
    open_ = close / (1 + returns)
    volume = rng.integers(1_000, 20_000, size=periods)
    df = pd.DataFrame(
        {
            "date": dates,
            "open": open_.round(2),
            "high": high.round(2),
            "low": low.round(2),
            "close": close.round(2),
            "volume": volume,
        }
    )
    _save(df, "bitcoin_prices.csv")


def generate_car_prices(n_samples: int = 400) -> None:
    rng = _rng()
    car_models = ["Swift", "City", "Corolla", "Civic", "Camry", "Fiesta", "Focus", "Altima"]
    fuel_types = ["Petrol", "Diesel", "CNG"]
    transmissions = ["Manual", "Automatic"]
    sellers = ["Dealer", "Individual"]
    owners = [0, 1, 2]

    years = rng.integers(2005, 2023, size=n_samples)
    base_price = 12 - 0.2 * (2023 - years) + rng.normal(0, 1.5, size=n_samples)
    present_price = np.clip(base_price + rng.normal(0, 1, size=n_samples), 1, None)
    kms_driven = rng.integers(5_000, 140_000, size=n_samples)
    selling_price = np.clip(
        present_price * rng.normal(0.55, 0.12, size=n_samples) - 0.00001 * kms_driven,
        0.5,
        None,
    )

    df = pd.DataFrame(
        {
            "car_name": rng.choice(car_models, size=n_samples),
            "year": years,
            "selling_price": selling_price.round(2),
            "present_price": present_price.round(2),
            "kms_driven": kms_driven,
            "fuel_type": rng.choice(fuel_types, size=n_samples),
            "seller_type": rng.choice(sellers, size=n_samples),
            "transmission": rng.choice(transmissions, size=n_samples),
            "owner": rng.choice(owners, size=n_samples),
        }
    )
    _save(df, "car_prices.csv")


def generate_movie_ratings(n_users: int = 100, n_movies: int = 40, density: float = 0.35) -> None:
    rng = _rng()
    users = np.arange(1, n_users + 1)
    movies = np.arange(1, n_movies + 1)
    mask = rng.random((n_users, n_movies)) < density
    rows = []
    for user_id, row in zip(users, mask):
        rated_movies = movies[row]
        for movie_id in rated_movies:
            rating = np.clip(rng.normal(3.5, 1.0), 0.5, 5.0)
            timestamp = rng.integers(1_600_000_000, 1_700_000_000)
            rows.append((user_id, movie_id, round(float(rating), 1), int(timestamp)))
    df = pd.DataFrame(rows, columns=["user_id", "movie_id", "rating", "timestamp"])
    _save(df, "movie_ratings.csv")


def generate_sp500_prices(n_symbols: int = 30, periods: int = 180) -> None:
    rng = _rng()
    symbols = [f"SYM{idx:03d}" for idx in range(1, n_symbols + 1)]
    dates = pd.date_range("2022-06-01", periods=periods, freq="B")
    rows = []
    for symbol in symbols:
        prices = 50 + np.cumsum(rng.normal(0, 1, size=periods))
        highs = prices + rng.normal(0.5, 0.3, size=periods)
        lows = prices - rng.normal(0.5, 0.3, size=periods)
        opens = prices + rng.normal(0, 0.5, size=periods)
        volumes = rng.integers(100_000, 2_000_000, size=periods)
        for date, open_, high, low, close, volume in zip(dates, opens, highs, lows, prices, volumes):
            rows.append(
                {
                    "date": date,
                    "symbol": symbol,
                    "open": round(float(open_), 2),
                    "high": round(float(high), 2),
                    "low": round(float(low), 2),
                    "close": round(float(close), 2),
                    "volume": int(volume),
                }
            )
    df = pd.DataFrame(rows)
    _save(df, "sp500_prices.csv")


def generate_house_prices(n_samples: int = 400) -> None:
    rng = _rng()
    neighborhoods = ["CollgCr", "Veenker", "Crawfor", "NoRidge", "Mitchel", "Somerst"]
    house_style = ["1Story", "2Story", "1.5Fin", "SLvl", "SFoyer"]
    lot_area = rng.normal(8_500, 2_000, size=n_samples).clip(3_000)
    overall_qual = rng.integers(3, 10, size=n_samples)
    year_built = rng.integers(1950, 2022, size=n_samples)
    gr_liv_area = rng.normal(1_700, 400, size=n_samples).clip(600)
    garage_cars = rng.integers(0, 4, size=n_samples)
    saleprice = (
        40_000
        + lot_area * 5
        + overall_qual * 20_000
        + (year_built - 1950) * 1_000
        + gr_liv_area * 80
        + garage_cars * 15_000
        + rng.normal(0, 20_000, size=n_samples)
    )
    df = pd.DataFrame(
        {
            "lot_area": lot_area.round(0).astype(int),
            "overall_qual": overall_qual,
            "year_built": year_built,
            "gr_liv_area": gr_liv_area.round(0).astype(int),
            "garage_cars": garage_cars,
            "neighborhood": rng.choice(neighborhoods, size=n_samples),
            "house_style": rng.choice(house_style, size=n_samples),
            "sale_price": saleprice.round(0).astype(int),
        }
    )
    _save(df, "house_prices.csv")


def generate_wine_quality(n_samples: int = 500) -> None:
    rng = _rng()
    fixed_acidity = rng.normal(8.5, 1.5, size=n_samples).clip(4, 15)
    volatile_acidity = rng.normal(0.5, 0.1, size=n_samples).clip(0.1, 1.5)
    citric_acid = rng.normal(0.3, 0.1, size=n_samples).clip(0.0, 1)
    residual_sugar = rng.normal(5, 2, size=n_samples).clip(0.6, 15)
    chlorides = rng.normal(0.07, 0.02, size=n_samples).clip(0.01, 0.2)
    free_sulfur = rng.normal(30, 10, size=n_samples).clip(5, 80)
    total_sulfur = free_sulfur + rng.normal(30, 10, size=n_samples)
    density = rng.normal(0.995, 0.003, size=n_samples)
    pH = rng.normal(3.3, 0.2, size=n_samples)
    sulphates = rng.normal(0.6, 0.1, size=n_samples)
    alcohol = rng.normal(10.5, 1.0, size=n_samples)
    quality = (
        3
        + 0.3 * alcohol
        - 0.5 * volatile_acidity
        + 0.1 * sulphates
        + rng.normal(0, 0.5, size=n_samples)
    ).round().clip(3, 8).astype(int)
    df = pd.DataFrame(
        {
            "fixed_acidity": fixed_acidity.round(2),
            "volatile_acidity": volatile_acidity.round(2),
            "citric_acid": citric_acid.round(2),
            "residual_sugar": residual_sugar.round(2),
            "chlorides": chlorides.round(3),
            "free_sulfur_dioxide": free_sulfur.round(1),
            "total_sulfur_dioxide": total_sulfur.round(1),
            "density": density.round(4),
            "pH": pH.round(2),
            "sulphates": sulphates.round(2),
            "alcohol": alcohol.round(2),
            "quality": quality,
        }
    )
    _save(df, "wine_quality.csv")


def generate_inventory_demand(n_stores: int = 10, n_items: int = 15, periods: int = 200) -> None:
    rng = _rng()
    dates = pd.date_range("2022-01-01", periods=periods, freq="D")
    rows = []
    for store in range(1, n_stores + 1):
        for item in range(1, n_items + 1):
            base_demand = rng.integers(20, 80)
            seasonal = 10 * np.sin(np.linspace(0, 3 * np.pi, periods))
            noise = rng.normal(0, 5, size=periods)
            sales = np.clip(base_demand + seasonal + noise, 0, None)
            for date, sale in zip(dates, sales):
                rows.append(
                    {
                        "date": date,
                        "store": store,
                        "item": item,
                        "units_sold": round(float(sale), 1),
                    }
                )
    df = pd.DataFrame(rows)
    _save(df, "inventory_demand.csv")


def generate_bike_fares(n_samples: int = 500) -> None:
    rng = _rng()
    cities = ["CDMX", "Bogota", "Lima", "Santiago", "BuenosAires"]
    ride_distance = rng.gamma(2.5, 1.2, size=n_samples)
    duration = ride_distance * rng.normal(7, 1, size=n_samples) + rng.normal(0, 5, size=n_samples)
    base_fare = 10 + ride_distance * 2.5 + duration * 0.3 + rng.normal(0, 3, size=n_samples)
    surge_multiplier = rng.choice([1.0, 1.25, 1.5], size=n_samples, p=[0.7, 0.2, 0.1])
    total_fare = base_fare * surge_multiplier
    df = pd.DataFrame(
        {
            "ride_id": np.arange(1, n_samples + 1),
            "city": rng.choice(cities, size=n_samples),
            "distance_km": ride_distance.round(2),
            "duration_min": duration.round(2),
            "surge_multiplier": surge_multiplier,
            "fare": total_fare.round(2),
        }
    )
    _save(df, "bike_fares.csv")


def generate_telco_churn(n_samples: int = 7043) -> None:
    rng = _rng()
    tenure = rng.integers(0, 73, size=n_samples)
    monthly_charges = rng.normal(70, 20, size=n_samples).clip(18, 120)
    contract = rng.choice(["Month-to-month", "One year", "Two year"], p=[0.6, 0.25, 0.15], size=n_samples)
    internet_service = rng.choice(["DSL", "Fiber optic", "None"], p=[0.35, 0.45, 0.2], size=n_samples)
    tech_support = rng.choice(["Yes", "No"], p=[0.3, 0.7], size=n_samples)
    senior = rng.choice(["Yes", "No"], p=[0.25, 0.75], size=n_samples)
    charges_total = tenure * monthly_charges + rng.normal(0, 50, size=n_samples)
    churn_prob = (
        0.25
        + 0.02 * (monthly_charges - 70)
        - 0.005 * tenure
        + 0.1 * (contract == "Month-to-month").astype(float)
        + 0.08 * (internet_service == "Fiber optic").astype(float)
        + 0.05 * (tech_support == "No").astype(float)
    )
    churn = rng.random(n_samples) < 1 / (1 + np.exp(-churn_prob))
    df = pd.DataFrame(
        {
            "customer_id": [f"C{idx:04d}" for idx in range(1, n_samples + 1)],
            "gender": rng.choice(["Male", "Female"], size=n_samples),
            "SeniorCitizen": (senior == "Yes").astype(int),
            "Partner": rng.choice(["Yes", "No"], size=n_samples),
            "Dependents": rng.choice(["Yes", "No"], size=n_samples),
            "tenure": tenure,
            "PhoneService": rng.choice(["Yes", "No"], p=[0.9, 0.1], size=n_samples),
            "MultipleLines": rng.choice(["Yes", "No", "No phone service"], size=n_samples),
            "InternetService": internet_service,
            "OnlineSecurity": rng.choice(["Yes", "No", "No internet service"], size=n_samples),
            "OnlineBackup": rng.choice(["Yes", "No", "No internet service"], size=n_samples),
            "DeviceProtection": rng.choice(["Yes", "No", "No internet service"], size=n_samples),
            "TechSupport": tech_support,
            "StreamingTV": rng.choice(["Yes", "No", "No internet service"], size=n_samples),
            "StreamingMovies": rng.choice(["Yes", "No", "No internet service"], size=n_samples),
            "Contract": contract,
            "PaperlessBilling": rng.choice(["Yes", "No"], size=n_samples),
            "PaymentMethod": rng.choice(
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                ],
                size=n_samples,
            ),
            "MonthlyCharges": monthly_charges.round(2),
            "TotalCharges": charges_total.round(2),
            "Churn": np.where(churn, "Yes", "No"),
        }
    )
    _save(df, "telco_churn.csv")


def generate_airline_delays(n_samples: int = 1500) -> None:
    rng = _rng()
    airlines = ["AA", "UA", "DL", "WN", "B6", "AS"]
    airports = ["ATL", "ORD", "LAX", "DFW", "DEN", "SFO", "SEA", "MIA"]
    weather = ["Clear", "Rain", "Snow", "Fog", "Storm"]
    dep_delay = rng.normal(5, 25, size=n_samples)
    arr_delay = dep_delay + rng.normal(0, 15, size=n_samples)
    cancellations = rng.choice([0, 1], p=[0.95, 0.05], size=n_samples)
    df = pd.DataFrame(
        {
            "flight_date": rng.choice(pd.date_range("2023-01-01", periods=200), size=n_samples),
            "airline": rng.choice(airlines, size=n_samples),
            "origin": rng.choice(airports, size=n_samples),
            "destination": rng.choice(airports, size=n_samples),
            "distance": rng.normal(900, 300, size=n_samples).clip(200, 2500).round(0),
            "weather": rng.choice(weather, size=n_samples, p=[0.6, 0.2, 0.05, 0.1, 0.05]),
            "departure_delay": dep_delay.round(1),
            "arrival_delay": arr_delay.round(1),
            "cancelled": cancellations,
        }
    )
    _save(df, "airline_delays.csv")


GENERATORS = [
    generate_bitcoin_prices,
    generate_car_prices,
    generate_movie_ratings,
    generate_sp500_prices,
    generate_house_prices,
    generate_wine_quality,
    generate_inventory_demand,
    generate_bike_fares,
    generate_telco_churn,
    generate_airline_delays,
]


def main() -> None:
    for generator in GENERATORS:
        generator()
    print(f"Generated {len(GENERATORS)} datasets in {DATA_DIR}.")


if __name__ == "__main__":
    main()
