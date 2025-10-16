"""Model service for loading and managing ML models."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.dataset_registry import DatasetInfo, TaskType, iter_datasets, get_dataset

# Path relativo desde api/services/ -> backend/reports/
MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "reports"

# Verificar si el path existe, si no, intentar con la nueva estructura
if not MODELS_DIR.exists():
    # Estamos en backend/api/services/, necesitamos backend/reports/
    MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "reports"
    
print(f"📂 Buscando modelos en: {MODELS_DIR}")
print(f"📂 Path existe: {MODELS_DIR.exists()}")


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
    
    def _to_snake_case(self, text: str) -> str:
        """
        Convert PascalCase/camelCase to snake_case.
        Examples:
            PaperlessBilling -> paperless_billing
            MonthlyCharges -> monthly_charges
            SeniorCitizen -> senior_citizen
        """
        import re
        # Insert underscore before uppercase letters that follow lowercase letters
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        # Insert underscore before uppercase letters that follow lowercase or numbers
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _clean_numeric_value(self, value: Any) -> Any:
        """
        Clean numeric values that might have commas or other formatting.
        Examples:
            "860,575,000" -> 860575000
            "45,535,800,000" -> 45535800000
        """
        if isinstance(value, str):
            # Remove commas and try to convert to float
            cleaned = value.replace(',', '')
            try:
                return float(cleaned)
            except ValueError:
                # If conversion fails, return original value (might be categorical)
                return value
        return value
    
    def _normalize_features(self, dataset_key: str, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize feature names and add model-specific features.
        
        Args:
            dataset_key: Key identifying the model
            features: Original feature dictionary
            
        Returns:
            Normalized feature dictionary with all required features
        """
        normalized = {}
        
        # Step 1: Normalize all incoming feature names and values
        for key, value in features.items():
            # Clean numeric values (remove commas)
            cleaned_value = self._clean_numeric_value(value)
            
            # Handle special cases first
            if key == "pH":
                normalized["p_h"] = cleaned_value
            elif key.startswith("4"):  # Avocado PLU codes (4046, 4225, 4770)
                normalized[f"col_{key}"] = cleaned_value
            else:
                # Standard normalization: 
                # 1. If key has spaces, just lowercase and replace spaces
                # 2. If key is PascalCase (no spaces), use to_snake_case
                if ' ' in key:
                    # Simple case: "Market Cap" -> "market_cap"
                    normalized_key = key.lower().replace(' ', '_')
                else:
                    # PascalCase: "PaperlessBilling" -> "paperless_billing"
                    normalized_key = self._to_snake_case(key)
                normalized[normalized_key] = cleaned_value
        
        # Step 2: Add model-specific engineered features
        # Note: For Bitcoin, lag_1, lag_7, and rolling_mean_7 should be provided by the user
        # as they represent historical price data that affects the prediction
        
        if dataset_key == "car_prices":
            # Car prices needs car_name
            if 'car_name' not in normalized:
                normalized['car_name'] = 'unknown'
        
        elif dataset_key == "telco_churn":
            # Telco needs customer_id (can be dummy for prediction)
            if 'customer_id' not in normalized:
                normalized['customer_id'] = 'PRED-0000'
        
        return normalized
    
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
        
        # Normalize features using model-specific logic
        normalized_features = self._normalize_features(dataset_key, features)
        
        print(f"📊 Original features: {list(features.keys())}")
        print(f"📊 Normalized features: {list(normalized_features.keys())}")
        
        # Convert features dict to DataFrame
        df = pd.DataFrame([normalized_features])
        
        # Make prediction
        if isinstance(model, Pipeline):
            prediction = model.predict(df)[0]
            
            # Convert numpy types to Python types for JSON serialization
            if hasattr(prediction, 'item'):
                # numpy scalar types have .item() method
                prediction = prediction.item()
            elif isinstance(prediction, np.generic):
                # For other numpy types
                prediction = prediction.tolist() if hasattr(prediction, 'tolist') else str(prediction)
            
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


# Global singleton instance
model_service = ModelService()
