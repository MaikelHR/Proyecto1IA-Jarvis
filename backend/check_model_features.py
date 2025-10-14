"""Script to check what features each model expects."""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dataset_registry import dataset_registry
import pandas as pd

def check_model_features():
    """Check what features each model expects."""
    
    for key, info in dataset_registry.items():
        print(f"\n{'='*80}")
        print(f"📊 {info.name} ({key})")
        print(f"{'='*80}")
        print(f"Tarea: {info.task.value}")
        print(f"Target: {info.target}")
        
        # Load data to see columns
        try:
            csv_path = Path(__file__).parent / info.data_path
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                
                # Remove target column
                features = [col for col in df.columns if col != info.target]
                
                print(f"\n✅ Features esperadas ({len(features)}):")
                for i, col in enumerate(features, 1):
                    # Get sample value
                    sample = df[col].iloc[0] if len(df) > 0 else "N/A"
                    dtype = df[col].dtype
                    print(f"  {i:2d}. {col:30s} | Tipo: {str(dtype):10s} | Ejemplo: {sample}")
                
                print(f"\n📋 Ejemplo de features dict para frontend:")
                example_dict = {}
                for col in features:
                    if df[col].dtype == 'object':
                        example_dict[col] = str(df[col].iloc[0])
                    else:
                        example_dict[col] = float(df[col].iloc[0])
                
                import json
                print(json.dumps(example_dict, indent=2, ensure_ascii=False))
                
            else:
                print(f"❌ Archivo no encontrado: {csv_path}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    check_model_features()
