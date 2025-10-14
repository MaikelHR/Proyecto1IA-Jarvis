"""Voice command processing service."""

from __future__ import annotations

import re
from typing import List, Optional


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


# Global singleton instance
voice_service = VoiceCommandService()
