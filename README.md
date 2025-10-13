# Proyecto Jarvis IA

Este repositorio contiene una versión reorganizada del asistente analítico
"Jarvis". La canalización procesa exclusivamente los conjuntos de datos
proporcionados en `data/raw/`, genera un resumen exploratorio y entrena un
modelo de *machine learning* apropiado para cada caso de uso.

## Estructura

```
├── data/
│   ├── README.md             # Documentación de los datos disponibles
│   └── raw/                  # Archivos CSV originales (no modificar)
├── reports/                  # Métricas y modelos generados automáticamente
├── requirements.txt          # Dependencias de Python
├── main.py                   # Punto de entrada CLI
└── src/
    ├── __init__.py
    ├── data_analysis.py      # Resúmenes exploratorios automatizados
    ├── data_loading.py       # Carga y limpieza específica por dataset
    ├── dataset_registry.py   # Metadatos y registro de datasets soportados
    ├── modeling.py           # Entrenamiento y evaluación de modelos
    └── pipeline.py           # Orquestador de la canalización
```

## Datasets soportados

La canalización incluye los siguientes casos de uso (clave entre paréntesis):

- Precio histórico de Bitcoin (`bitcoin_price`) – serie temporal con ingeniería
  de *lags*.
- Precios de aguacate por región (`avocado_prices`) – regresión multivariante.
- Porcentaje de grasa corporal (`body_fat`) – regresión.
- Valor de automóviles usados (`car_prices`) – regresión.
- Churn de clientes Telco (`telco_churn`) – clasificación binaria.
- Calidad de vinos (`wine_quality`) – clasificación multiclase.
- Predicción de derrame cerebral (`stroke_risk`) – clasificación binaria.
- Diagnóstico de hepatitis C (`hepatitis_c`) – clasificación multiclase.
- Estatus clínico de cirrosis (`cirrhosis_status`) – clasificación multiclase.

## Requisitos

```bash
pip install -r requirements.txt
```

## Uso

Ejecutar todos los análisis y modelos:

```bash
python main.py
```

Procesar solamente un dataset específico (por ejemplo `telco_churn`):

```bash
python main.py --dataset telco_churn
```

Los resúmenes exploratorios y métricas se guardan en `reports/` usando nombres
basados en el archivo fuente. Los modelos entrenados se serializan en formato
`pickle` dentro del mismo directorio.

## Notas

- No se generan datos sintéticos. Todos los experimentos utilizan únicamente los
  CSV almacenados en `data/raw/`.
- Evite versionar artefactos derivados distintos de los definidos en este
  repositorio. La canalización permite recrearlos cuando sea necesario.
