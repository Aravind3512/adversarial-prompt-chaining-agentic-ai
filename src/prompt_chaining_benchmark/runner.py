"""Experiment runner helpers."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .data import Task, generate_dataset, save_jsonl
from .metrics import summarize_by_ratio
from .pipeline import AgentState, run_pipeline

DEFAULT_RATIOS = [0.05, 0.10, 0.20, 0.30]


def run_experiment(
    poison_ratios: Iterable[float] = DEFAULT_RATIOS,
    total_tasks: int = 100,
    seed: int = 6730,
    backend: str = "deterministic",
) -> tuple[list[Task], list[AgentState], list[dict]]:
    tasks: list[Task] = []
    states: list[AgentState] = []
    for ratio in poison_ratios:
        ratio_tasks = generate_dataset(ratio, total_tasks=total_tasks, seed=seed)
        tasks.extend(ratio_tasks)
        states.extend(run_pipeline(task, backend=backend) for task in ratio_tasks)
    metrics = summarize_by_ratio(states)
    return tasks, states, metrics


def save_outputs(tasks: list[Task], states: list[AgentState], metrics: list[dict], output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    save_jsonl(tasks, output / "tasks.jsonl")

    with (output / "traces.jsonl").open("w", encoding="utf-8") as handle:
        for state in states:
            handle.write(json.dumps(state.to_dict(), ensure_ascii=False) + "\n")

    if metrics:
        fieldnames = list(metrics[0].keys())
        with (output / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(metrics)
