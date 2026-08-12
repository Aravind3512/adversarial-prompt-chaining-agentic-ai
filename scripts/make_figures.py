#!/usr/bin/env python3
"""Generate figures from benchmark metrics."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from prompt_chaining_benchmark.plotting import plot_asr, plot_propagation, plot_safety, read_metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create benchmark figures from metrics.csv.")
    parser.add_argument("--metrics", default="results/full/metrics.csv", help="Path to metrics.csv")
    parser.add_argument("--output", default="results/figures", help="Directory for generated figures")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics_path = ROOT / args.metrics
    output_dir = ROOT / args.output
    rows = read_metrics(metrics_path)
    written = [plot_asr(rows, output_dir), *plot_safety(rows, output_dir), plot_propagation(rows, output_dir)]
    print("Generated figures:")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
