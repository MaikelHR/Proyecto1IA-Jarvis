"""Business logic services for the Jarvis API."""

from __future__ import annotations

import pickle
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.dataset_registry import DatasetInfo, TaskType, iter_datasets, get_dataset

MODELS_DIR = Path(__file__).resolve().parent.parent / "reports"


class ModelService:
    """Service for loading and managing ML models."""
    
    def __init__(self):
        self._models: Dict[str, Any] = {}
        self._dataset_info: Dict[str, DatasetInfo] = {}
        self._load_all_models()
    
    def _load_all_models(self) -> None:
        """Load all trained models from disk."""
        for dataset_info in iter_datasets():
            try:
                # Determine model file path
                if dataset_info.task == TaskType.TIME_SERIES:
                    model_path = MODELS_DIR / f"{dataset_info.path.stem}_model.pkl"
                else:
                    model_path = MODELS_DIR / f"{dataset_info.path.stem}_model.pkl"
                
                # Check for recommender systems
                recommender_path = MODELS_DIR / f"{dataset_info.path.stem}_recommender.pkl"
                if recommender_path.exists():
                    model_path = recommender_path
                
                if model_path.exists():
                    with open(model_path, "rb") as f:
                        model = pickle.load(f)
                    
                    key = self._get_dataset_key(dataset_info.name)
                    self._models[key] = model
                    self._dataset_info[key] = dataset_info
                    print(f"✓ Modelo cargado: {dataset_info.name} ({key})")
                else:
                    print(f"⚠ Modelo no encontrado: {model_path}")
            except Exception as e:
                print(f"✗ Error cargando {dataset_info.name}: {e}")
    
    @staticmethod
    def _get_dataset_key(name: str) -> str:
        """Convert dataset name to key format."""
        # Map known dataset names to keys
        mapping = {
            "Precio histórico de Bitcoin": "bitcoin_price",
            "Precios de aguacate por región": "avocado_prices",
            "Porcentaje de grasa corporal": "body_fat",
            "Valor de automóviles usados": "car_prices",
            "Churn de clientes Telco": "telco_churn",
            "Calidad de vinos": "wine_quality",
            "Predicción de derrame cerebral": "stroke_risk",
            "Diagnóstico de hepatitis C": "hepatitis_c",
            "Estatus clínico de cirrosis": "cirrhosis_status",
        }
        return mapping.get(name, name.lower().replace(" ", "_"))
    
    def get_available_models(self) -> List[str]:
        """Get list of available model keys."""
        return list(self._models.keys())
    
    def get_model_info(self, dataset_key: str) -> Optional[DatasetInfo]:
        """Get information about a specific dataset."""
        return self._dataset_info.get(dataset_key)
    
    def predict(self, dataset_key: str, features: Dict[str, Any]) -> Tuple[Any, Optional[float]]:
        """
        Make a prediction using the specified model.
        
        Args:
            dataset_key: Key identifying the model to use
            features: Dictionary of feature values
            
        Returns:
            Tuple of (prediction, confidence)
        """
        if dataset_key not in self._models:
            raise ValueError(f"Model '{dataset_key}' not found. Available: {self.get_available_models()}")
        
        model = self._models[dataset_key]
        dataset_info = self._dataset_info[dataset_key]
        
        # Convert features dict to DataFrame
        df = pd.DataFrame([features])
        
        # Make prediction
        if isinstance(model, Pipeline):
            prediction = model.predict(df)[0]
            
            # Get confidence for classification
            confidence = None
            if dataset_info.task == TaskType.CLASSIFICATION and hasattr(model, 'predict_proba'):
                try:
                    proba = model.predict_proba(df)[0]
                    confidence = float(np.max(proba))
                except Exception:
                    pass
            
            return prediction, confidence
        
        elif isinstance(model, dict):  # Recommender system
            # Handle recommendation prediction
            user_id = features.get("user_id")
            movie_id = features.get("movie_id")
            
            if user_id is None or movie_id is None:
                raise ValueError("Recommender requires 'user_id' and 'movie_id'")
            
            global_mean = model["global_mean"]
            user_bias = model["user_means"].get(user_id, global_mean) - global_mean
            movie_bias = model["movie_means"].get(movie_id, global_mean) - global_mean
            prediction = global_mean + user_bias + movie_bias
            
            return float(prediction), None
        
        else:
            raise ValueError(f"Unknown model type: {type(model)}")
    
    def get_models_count(self) -> int:
        """Get the number of loaded models."""
        return len(self._models)


class VoiceCommandService:
    """Service for processing voice commands."""
    
    # Command patterns mapping to dataset keys
    COMMAND_PATTERNS = {
        "bitcoin_price": [
            r"(predice|predicción|precio).*(bitcoin|btc)",
            r"bitcoin.*(mañana|precio|predicción)",
        ],
        "avocado_prices": [
            r"(predice|predicción|precio).*(aguacate|palta)",
            r"aguacate.*(precio|predicción)",
        ],
        "body_fat": [
            r"(calcula|predice).*(grasa\s*corporal|porcentaje.*grasa)",
            r"grasa\s*corporal",
        ],
        "car_prices": [
            r"(valora|precio|valor).*(auto|carro|vehículo|automóvil)",
            r"(auto|carro).*(usado|precio)",
        ],
        "telco_churn": [
            r"(predice|analiza).*(churn|abandono|retención)",
            r"(cliente|usuario).*(abandono|churn)",
        ],
        "wine_quality": [
            r"(evalúa|calidad).*(vino)",
            r"vino.*(calidad|evaluación)",
        ],
        "stroke_risk": [
            r"(evalúa|predice|riesgo).*(derrame|cerebral|stroke|ictus)",
            r"derrame.*(cerebral|predicción)",
        ],
        "hepatitis_c": [
            r"(diagnostica|diagnóstico).*(hepatitis)",
            r"hepatitis.*(c|predicción)",
        ],
        "cirrhosis_status": [
            r"(analiza|estado|estatus).*(cirrosis|hepática)",
            r"cirrosis.*(estado|predicción)",
        ],
    }
    
    @classmethod
    def parse_command(cls, transcript: str) -> Optional[str]:
        """
        Parse voice transcript to identify dataset command.
        
        Args:
            transcript: Transcribed text from speech
            
        Returns:
            Dataset key if command recognized, None otherwise
        """
        # Normalize transcript
        text = transcript.lower().strip()
        
        # Remove common prefixes
        text = re.sub(r"^(jarvis|hey jarvis|ok jarvis)[,\s]*", "", text)
        
        # Try to match patterns
        for dataset_key, patterns in cls.COMMAND_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return dataset_key
        
        return None
    
    @classmethod
    def get_command_examples(cls, dataset_key: str) -> List[str]:
        """Get example voice commands for a dataset."""
        examples_map = {
            "bitcoin_price": [
                "Jarvis, predice el precio de Bitcoin",
                "¿Cuál será el precio de Bitcoin mañana?"
            ],
            "avocado_prices": [
                "Jarvis, predice el precio del aguacate",
                "¿Cuánto costará el aguacate?"
            ],
            "body_fat": [
                "Jarvis, calcula mi grasa corporal",
                "¿Cuál es mi porcentaje de grasa?"
            ],
            "car_prices": [
                "Jarvis, valora este auto usado",
                "¿Cuánto vale este vehículo?"
            ],
            "telco_churn": [
                "Jarvis, analiza riesgo de churn",
                "¿Este cliente abandonará el servicio?"
            ],
            "wine_quality": [
                "Jarvis, evalúa la calidad del vino",
                "¿Qué calidad tiene este vino?"
            ],
            "stroke_risk": [
                "Jarvis, evalúa riesgo de derrame cerebral",
                "¿Cuál es el riesgo de stroke?"
            ],
            "hepatitis_c": [
                "Jarvis, diagnostica hepatitis C",
                "Analiza estos resultados de laboratorio"
            ],
            "cirrhosis_status": [
                "Jarvis, analiza el estado de cirrosis",
                "¿Cuál es el estatus clínico?"
            ],
        }
        return examples_map.get(dataset_key, ["No examples available"])


# Global singleton instances
model_service = ModelService()
voice_service = VoiceCommandService()
