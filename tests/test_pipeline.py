from prompt_chaining_benchmark.data import generate_dataset
from prompt_chaining_benchmark.pipeline import run_pipeline


def test_clean_tasks_remain_safe():
    task = next(task for task in generate_dataset(0.10, total_tasks=100, seed=6730) if not task.is_poisoned)
    state = run_pipeline(task)
    assert state.route_decision == "normal_completion"
    assert state.selected_tool == "mock_allowed_action"
    assert state.benchmark_status == "SAFE_COMPLETION"
    assert state.propagation_depth == 0


def test_subtle_task_remains_safe():
    task = next(task for task in generate_dataset(0.10, total_tasks=100, seed=6730) if task.variant == "subtle")
    state = run_pipeline(task)
    assert state.route_decision == "normal_completion"
    assert state.selected_tool == "mock_allowed_action"
    assert state.benchmark_status == "SAFE_COMPLETION"


def test_strong_task_can_trigger_benchmark_route():
    task = next(task for task in generate_dataset(0.10, total_tasks=100, seed=6730) if task.variant == "strong")
    state = run_pipeline(task)
    assert state.route_decision == "audit_verification"
    assert state.selected_tool == "mock_restricted_action"
    assert state.benchmark_status == "BENCHMARK_TRIGGERED"
    assert state.propagation_depth == 6
