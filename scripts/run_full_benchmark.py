#!/usr/bin/env python3
"""Run the full deterministic benchmark for the four presentation ratios."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from prompt_chaining_benchmark.runner import DEFAULT_RATIOS, run_experiment, save_outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the synthetic prompt-chaining benchmark.")
    parser.add_argument("--output", default="results/full", help="Output directory for tasks, traces, and metrics.")
    parser.add_argument("--tasks-per-ratio", type=int, default=100, help="Number of tasks per poison ratio.")
    parser.add_argument("--seed", type=int, default=6730, help="Dataset seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tasks, states, metrics = run_experiment(DEFAULT_RATIOS, total_tasks=args.tasks_per_ratio, seed=args.seed)
    output_dir = ROOT / args.output
    save_outputs(tasks, states, metrics, output_dir)
    print(f"Full benchmark complete: {len(tasks)} tasks, {len(states)} traces")
    print(f"Wrote outputs to {output_dir}")
    for row in metrics:
        print(
            f"ratio={row['poison_ratio']:.2f} poisoned={row['poisoned_tasks']} "
            f"err={row['error_rate']:.2f} asr_strict={row['asr_strict']:.2f} "
            f"overall={row['overall_failure_rate']:.2f} benign={row['benign_utility']:.2f} "
            f"depth={row['avg_propagation_depth']:.2f}"
        )


if __name__ == "__main__":
    main()
