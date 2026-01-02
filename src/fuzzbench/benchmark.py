import json, os, random, time, psutil
from . import baseline_impl, impl


def _rss_mb():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)


def _gen(seed, n_c, n_q, L):
    rng = random.Random(seed)
    abc = "abcdefghijklmnopqrstuvwxyz"

    def s():
        return "".join(rng.choice(abc) for _ in range(L))

    choices = [s() for _ in range(n_c)]
    queries = []
    for _ in range(n_q):
        base = list(rng.choice(choices))
        for _ in range(max(1, L // 10)):
            i = rng.randrange(L)
            base[i] = rng.choice(abc)
        queries.append("".join(base))
    return queries, choices


def run_benchmark(out_json="artifacts/perf_report.json"):
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    queries, choices = _gen(1337, 1200, 60, 40)

    t0, r0 = time.perf_counter(), _rss_mb()
    baseline_impl.batch_best_match(queries, choices)
    t1, r1 = time.perf_counter(), _rss_mb()

    t2, r2 = time.perf_counter(), _rss_mb()
    impl.batch_best_match(queries, choices)
    t3, r3 = time.perf_counter(), _rss_mb()

    report = {
        "baseline_time_s": t1 - t0,
        "optimized_time_s": t3 - t2,
        "speedup": (t1 - t0) / (t3 - t2),
        "baseline_rss_mb": r1,
        "optimized_rss_mb": r3,
    }

    with open(out_json, "w") as f:
        json.dump(report, f, indent=2)

    return report
