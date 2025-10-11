"""Command line entry point for running analyses and models."""

from __future__ import annotations

import argparse
from typing import Iterable

from .dataset_registry import DatasetInfo, get_dataset, iter_datasets
from .data_analysis import summarize_dataset
from .modeling import save_model_result, train_dataset


def _run_dataset(dataset: DatasetInfo) -> None:
    summary_path = summarize_dataset(dataset)
    result = train_dataset(dataset)
    metrics_path = save_model_result(result)
    print(f"Resumen guardado en {summary_path}")
    print(f"Métricas guardadas en {metrics_path}")


def run(datasets: Iterable[DatasetInfo]) -> None:
    for dataset in datasets:
        print("=" * 80)
        print(f"Procesando: {dataset.name}")
        _run_dataset(dataset)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pipeline de análisis y modelado Jarvis")
    parser.add_argument(
        "--dataset",
        dest="dataset",
        default=None,
        help="Clave del dataset a ejecutar. Si se omite se procesan todos.",
    )
    return parser


def main() -> None:
    parser = build_argument_parser()
    args = parser.parse_args()
    if args.dataset:
        dataset = get_dataset(args.dataset)
        run([dataset])
    else:
        run(iter_datasets())


if __name__ == "__main__":
    main()
