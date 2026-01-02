from fuzzbench.benchmark import run_benchmark


def test_speed():
    r = run_benchmark()
    assert r["optimized_time_s"] <= 0.35
    assert r["speedup"] >= 12.0
