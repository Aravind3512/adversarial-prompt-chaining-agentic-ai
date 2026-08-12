#!/usr/bin/env python3
"""Run a small deterministic smoke test."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from prompt_chaining_benchmark.runner import run_experiment, save_outputs


def main() -> None:
    tasks, states, metrics = run_experiment(poison_ratios=[0.10], total_tasks=100, seed=6730)
    output_dir = ROOT / "results" / "smoke"
    save_outputs(tasks, states, metrics, output_dir)
    print("Smoke run complete")
    print(f"tasks={len(tasks)} traces={len(states)} output={output_dir}")
    for row in metrics:
        print(
            f"poison_ratio={row['poison_ratio']:.2f} "
            f"asr_strict={row['asr_strict']:.2f} "
            f"benign_utility={row['benign_utility']:.2f} "
            f"error_rate={row['error_rate']:.2f}"
        )


if __name__ == "__main__":
    main()
