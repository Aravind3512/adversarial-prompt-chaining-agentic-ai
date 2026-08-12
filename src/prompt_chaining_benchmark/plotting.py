"""Figure generation for benchmark outputs."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


def read_metrics(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [{key: _coerce(value) for key, value in row.items()} for row in reader]


def _coerce(value: str):
    try:
        return float(value)
    except ValueError:
        return value


def plot_asr(metrics: list[dict], output_dir: str | Path) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    ratios = [row["poison_ratio"] for row in metrics]
    asr_tool = [row["asr_tool"] for row in metrics]
    asr_strict = [row["asr_strict"] for row in metrics]

    plt.figure(figsize=(7, 4.5))
    plt.plot(ratios, asr_tool, marker="o", label="ASR Tool")
    plt.plot(ratios, asr_strict, marker="o", label="ASR Strict")
    plt.xlabel("Poison ratio")
    plt.ylabel("ASR on poisoned tasks")
    plt.title("Strict ASR vs Distributed Poison Ratio")
    plt.grid(True, alpha=0.3)
    plt.legend()
    path = output / "asr_vs_poison_ratio.png"
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def plot_safety(metrics: list[dict], output_dir: str | Path) -> list[Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    ratios = [row["poison_ratio"] for row in metrics]
    benign = [row["benign_utility"] for row in metrics]
    overall = [row["overall_failure_rate"] for row in metrics]

    paths: list[Path] = []
    plt.figure(figsize=(7, 4.5))
    plt.plot(ratios, benign, marker="o")
    plt.xlabel("Poison ratio")
    plt.ylabel("Benign utility")
    plt.title("Benign Utility vs Poison Ratio")
    plt.grid(True, alpha=0.3)
    path = output / "benign_utility_vs_poison_ratio.png"
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    paths.append(path)

    plt.figure(figsize=(7, 4.5))
    plt.plot(ratios, overall, marker="o")
    plt.xlabel("Poison ratio")
    plt.ylabel("Overall failure rate")
    plt.title("Overall Failure Rate vs Poison Ratio")
    plt.grid(True, alpha=0.3)
    path = output / "overall_failure_vs_poison_ratio.png"
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    paths.append(path)
    return paths


def plot_propagation(metrics: list[dict], output_dir: str | Path) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    ratios = [row["poison_ratio"] for row in metrics]
    series = [
        ("summarizer_retention_rate", "Summarizer retention"),
        ("policy_retention_rate", "Policy retention"),
        ("routing_trigger_rate", "Routing trigger"),
        ("restricted_tool_rate", "Restricted tool"),
        ("final_trigger_rate", "Final trigger"),
    ]
    plt.figure(figsize=(8, 4.8))
    for key, label in series:
        plt.plot(ratios, [row[key] for row in metrics], marker="o", label=label)
    plt.xlabel("Poison ratio")
    plt.ylabel("Rate on poisoned tasks")
    plt.title("Intermediate Propagation Metrics")
    plt.grid(True, alpha=0.3)
    plt.legend()
    path = output / "intermediate_propagation_metrics.png"
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    return path
