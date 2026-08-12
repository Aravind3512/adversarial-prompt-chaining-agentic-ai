# Validation Log

Validation completed for the GitHub-ready repository.

Commands run from repository root:

```bash
python -m compileall src scripts
PYTHONPATH=src pytest -q
python scripts/run_smoke.py
python scripts/run_full_benchmark.py --output results/full
python scripts/make_figures.py --metrics results/full/metrics.csv --output results/figures
```

Observed results:

```text
7 passed
Smoke run complete
poison_ratio=0.10 asr_strict=0.30 benign_utility=1.00 error_rate=0.00
Full benchmark complete: 400 tasks, 400 traces
ratio=0.05 poisoned=5 err=0.00 asr_strict=0.00 overall=0.00 benign=1.00 depth=2.60
ratio=0.10 poisoned=10 err=0.00 asr_strict=0.30 overall=0.03 benign=1.00 depth=3.50
ratio=0.20 poisoned=20 err=0.00 asr_strict=0.30 overall=0.06 benign=1.00 depth=3.55
ratio=0.30 poisoned=30 err=0.00 asr_strict=0.30 overall=0.09 benign=1.00 depth=3.57
```

The notebooks were checked as valid JSON notebooks with no saved execution outputs.

The default implementation is deterministic and does not require Ollama, GPU access, model downloads, or external APIs. The optional Ollama helper was not end-to-end tested in this environment.
