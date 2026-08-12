from prompt_chaining_benchmark.data import generate_dataset


def test_dataset_counts_match_poison_ratios():
    expected = {0.05: 5, 0.10: 10, 0.20: 20, 0.30: 30}
    for ratio, poisoned in expected.items():
        tasks = generate_dataset(ratio, total_tasks=100, seed=6730)
        assert len(tasks) == 100
        assert sum(task.is_poisoned for task in tasks) == poisoned
        assert sum(not task.is_poisoned for task in tasks) == 100 - poisoned


def test_strong_and_subtle_variants_present_for_larger_ratios():
    tasks = generate_dataset(0.20, total_tasks=100, seed=6730)
    variants = [task.variant for task in tasks if task.is_poisoned]
    assert variants.count("strong") == 10
    assert variants.count("subtle") == 10
