# Proyecto Jarvis IA

Este repositorio contiene una versión simplificada del asistente inteligente
solicitado en el enunciado. Se generan 10 conjuntos de datos sintéticos que
representan las problemáticas propuestas (precios, churn, inventarios, etc.),
se realiza un análisis exploratorio automatizado y se entrenan modelos de
aprendizaje automático apropiados para cada tarea.

## Estructura

- `scripts/generate_synthetic_datasets.py`: genera los 10 *datasets* a partir de
  distribuciones controladas.
- `src/dataset_registry.py`: catálogo de metadatos para cada *dataset*.
- `src/data_analysis.py`: utilidades de análisis exploratorio.
- `src/modeling.py`: entrenamiento y evaluación de modelos.
- `src/pipeline.py`: orquestador CLI que ejecuta análisis y entrenamiento.
- `data/`: se genera al ejecutar el script y queda vacío en Git (ver sección de control de versiones).
- `reports/`: directorio de salida para métricas/modelos (ignorado en Git).

## Requisitos

```bash
pip install -r requirements.txt
```

## Uso

Generar/recrear los *datasets* y ejecutar la canalización completa:

```bash
python scripts/generate_synthetic_datasets.py
python main.py
```

Para procesar solo un conjunto de datos específico (por ejemplo `telco_churn`):

```bash
python main.py --dataset telco_churn
```

Los reportes se guardan en el directorio `reports/` y los modelos entrenados en
formato `pickle`.

## Notas sobre control de versiones

- Los archivos generados en `data/` y `reports/` se excluyen del control de versiones. 
  Ejecute los scripts para recrearlos localmente cuando sea necesario, pero no los suba al repositorio.
- Antes de abrir un Pull Request, asegúrese de que el proyecto corre correctamente ejecutando
  `python scripts/generate_synthetic_datasets.py` y `python main.py`; esto valida que el código
  continúe produciendo los artefactos requeridos sin necesidad de almacenarlos en Git.

