from prompt_chaining_benchmark.runner import DEFAULT_RATIOS, run_experiment


def test_reference_metrics_match_presentation_values():
    _, _, metrics = run_experiment(DEFAULT_RATIOS, total_tasks=100, seed=6730)
    by_ratio = {round(row["poison_ratio"], 2): row for row in metrics}

    assert by_ratio[0.05]["poisoned_tasks"] == 5
    assert by_ratio[0.05]["asr_strict"] == 0.0
    assert round(by_ratio[0.05]["avg_propagation_depth"], 2) == 2.60

    for ratio, depth in [(0.10, 3.50), (0.20, 3.55), (0.30, 3.57)]:
        assert by_ratio[ratio]["error_rate"] == 0.0
        assert round(by_ratio[ratio]["asr_tool"], 2) == 0.30
        assert round(by_ratio[ratio]["asr_final"], 2) == 0.30
        assert round(by_ratio[ratio]["asr_strict"], 2) == 0.30
        assert by_ratio[ratio]["benign_utility"] == 1.0
        assert round(by_ratio[ratio]["avg_propagation_depth"], 2) == depth


def test_overall_failure_scales_with_ratio():
    _, _, metrics = run_experiment(DEFAULT_RATIOS, total_tasks=100, seed=6730)
    overall = [round(row["overall_failure_rate"], 2) for row in metrics]
    assert overall == [0.00, 0.03, 0.06, 0.09]
