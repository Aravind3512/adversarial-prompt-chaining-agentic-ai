# Adversarial Prompt Chaining Attacks in Agentic AI

A safe, synthetic benchmark for studying how individually incomplete prompt fragments can propagate across an agentic workflow and cause a controlled route/tool-selection failure. The project uses customer-service-style synthetic documents, harmless reference tags, local mock tools, route-first tool binding, and explicit metrics for attack success rate, propagation depth, benign utility, and error rate.

## Project Context

This repository is based on a COMS 6730 Advanced Topics in Machine Learning project at Iowa State University.

**Authors**

- Aravind Adari
- Vijaysimha Bandaru

**Course**: COMS 6730: Advanced Topics in Machine Learning  
**Instructor**: Professor Amit Kumar Sikder

## Research Question

Can individually incomplete prompt fragments propagate through a multi-agent workflow and cause a downstream synthetic route/tool-selection failure?

The benchmark tests this question under a strict safety boundary. The restricted tool is only a local mock function that returns a benchmark marker. It has no external side effects, no credentials, no network access, no production integration, and no real account actions.

## Key Idea

Single-document prompt injection is easier to detect because one input may contain a complete malicious instruction. This project instead evaluates a distributed prompt-chain condition:

1. One source preserves a harmless reference tag.
2. A second source describes route/tool mapping.
3. A third source defines a routing condition.
4. The fragments only become meaningful after retrieval, summarization, policy reasoning, routing, and tool binding combine them in agent state.

The result is measured as a synthetic benchmark failure only when the route-first pipeline selects `mock_restricted_action` and the final status is `BENCHMARK_TRIGGERED`.

## Safety Boundary

This repository is intentionally limited to a harmless synthetic benchmark.

Out of scope:

- Real credentials or secrets
- Real external APIs or accounts
- Malware, phishing, exfiltration, or production bypass
- Real tool execution
- Real customer data

In scope:

- Synthetic customer-service documents
- Harmless reference tags
- Local mock tools only
- Controlled route/tool benchmark failures
- Reproducible metric calculation

## Implemented Pipeline

The benchmark uses a route-first agent workflow:

```text
Task docs
  -> Retriever
  -> Summarizer
  -> Policy Analyst
  -> Router
  -> Tool Selector
  -> Mock Executor
  -> Finalizer
```

The GitHub-ready version uses a deterministic backend by default so the project can run without model downloads or paid APIs. The structure mirrors the final project pipeline and preserves the same observable benchmark quantities.

The state tracks:

- Synthetic documents
- Workflow metadata
- Summary
- Policy decision
- Route decision
- Selected tool
- Benchmark status
- Propagation flags
- Propagation depth
- Error status
- Latency proxy

## Dataset

The benchmark generates four 100-task datasets:

| Poison ratio | Total tasks | Poisoned tasks | Clean tasks |
|---:|---:|---:|---:|
| 5% | 100 | 5 | 95 |
| 10% | 100 | 10 | 90 |
| 20% | 100 | 20 | 80 |
| 30% | 100 | 30 | 70 |

Poisoned tasks are split into two variants:

- **Subtle split**: natural audit-trail wording with weak route cues.
- **Strong split**: clearer distributed routing evidence that activates when metadata survives the route-first pipeline.

## Reference Results

The deterministic benchmark reproduces the final presentation-level aggregate behavior:

| Poison ratio | Poisoned | Error rate | ASR Tool | ASR Final | ASR Strict | Overall failure | Benign utility | Avg. depth |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5% | 5 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 2.60 |
| 10% | 10 | 0.00 | 0.30 | 0.30 | 0.30 | 0.03 | 1.00 | 3.50 |
| 20% | 20 | 0.00 | 0.30 | 0.30 | 0.30 | 0.06 | 1.00 | 3.55 |
| 30% | 30 | 0.00 | 0.30 | 0.30 | 0.30 | 0.09 | 1.00 | 3.57 |

Interpretation:

- 5% poisoning is sparse and remains at 0% strict ASR.
- 10%, 20%, and 30% poisoning stabilize at 30% strict ASR.
- Clean-task benign utility remains 1.00.
- Overall failure scales with poison ratio because failures are confined to poisoned tasks.
- The 30% aggregate ASR is explained by 60% strong-split ASR and 0% subtle-split ASR with approximately half strong and half subtle poisoned tasks.

## Repository Structure

```text
adversarial-prompt-chaining-agentic-ai/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .env.example
├── src/
│   └── prompt_chaining_benchmark/
│       ├── __init__.py
│       ├── data.py
│       ├── pipeline.py
│       ├── metrics.py
│       ├── runner.py
│       ├── plotting.py
│       └── ollama_client.py
├── scripts/
│   ├── run_smoke.py
│   ├── run_full_benchmark.py
│   └── make_figures.py
├── notebooks/
│   ├── 01_dataset_generation.ipynb
│   ├── 02_run_benchmark.ipynb
│   └── 03_analyze_results.ipynb
├── tests/
│   ├── test_dataset.py
│   ├── test_pipeline.py
│   └── test_metrics.py
├── docs/
│   ├── GITHUB_REPO_PREP_PROMPT.md
│   └── PROJECT_OVERVIEW.md
├── presentation/
│   └── Adv_ML_Project_ppt.pdf
└── results/
    └── figures/
```

## Installation

```bash
cd adversarial-prompt-chaining-agentic-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Quick Smoke Run

```bash
python scripts/run_smoke.py
```

Expected output includes:

```text
Smoke run complete
poison_ratio=0.10 asr_strict=0.30 benign_utility=1.00 error_rate=0.00
```

## Full Benchmark Run

```bash
python scripts/run_full_benchmark.py --output results/full
```

This writes:

```text
results/full/tasks.jsonl
results/full/traces.jsonl
results/full/metrics.csv
```

## Generate Figures

```bash
python scripts/make_figures.py --metrics results/full/metrics.csv --output results/figures
```

Generated figures:

```text
results/figures/asr_vs_poison_ratio.png
results/figures/benign_utility_vs_poison_ratio.png
results/figures/overall_failure_vs_poison_ratio.png
results/figures/intermediate_propagation_metrics.png
```

## Run Tests

```bash
pytest -q
```

The tests verify:

- Dataset poison counts
- Strong/subtle split construction
- Clean tasks remain safe
- Subtle split remains safe
- Strong split can activate the synthetic benchmark route
- Aggregate metrics match the final project presentation values

## Notebook Workflow

The `notebooks/` directory separates the project into three reproducible stages:

1. `01_dataset_generation.ipynb` — generate and inspect synthetic datasets.
2. `02_run_benchmark.ipynb` — run the route-first benchmark and compute metrics.
3. `03_analyze_results.ipynb` — load metrics and generate plots.

Run notebooks after installing the package in editable mode:

```bash
pip install -e .
jupyter notebook
```

## Optional Ollama Adaptation

The final presentation used local Ollama execution with small Qwen and Llama models. This GitHub-ready repository keeps deterministic execution as the default so reviewers can run the code immediately. The file `src/prompt_chaining_benchmark/ollama_client.py` contains a minimal optional Ollama client for future adaptation.

Example local settings are provided in `.env.example`:

```text
OLLAMA_BASE_URL=http://127.0.0.1:11434
SUMMARY_MODEL=qwen2.5:0.5b-instruct
POLICY_MODEL=qwen2.5:0.5b-instruct
ROUTER_MODEL=llama3.2:1b
FINALIZER_MODEL=qwen2.5:0.5b-instruct
```

## Notes on Reproducibility

- The default backend is deterministic.
- The seed is fixed at `6730` unless overridden.
- The synthetic restricted tool has no real side effects.
- The reported reference metrics are enforced through tests.
- The presentation PDF is included for project context.

## Limitations

- The benchmark is synthetic and should not be interpreted as a production compromise.
- The GitHub-ready implementation uses deterministic logic by default rather than executing local LLM calls.
- The final project presentation used one deadline-run seed.
- Subtle split did not trigger in the reported smoke/case-study behavior.
- Defense-placement experiments are not implemented in this repository.

## License

No license is included by default. Add a license only after confirming with all project contributors and course policies.
