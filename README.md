# fuzzbench — optimized batch matching

## Quickstart ✅

- Create venv, install deps, and run tests:

```bash
./run_tests
```

(This will create `.venv`, install pinned dependencies from `requirements.txt`, and run the full test suite.)

## What I changed 🔧

- Implemented an optimized `batch_best_match` in `src/fuzzbench/impl.py` using `rapidfuzz`'s C-accelerated `Levenshtein.distance` to compute exact edit distances and derive the same score as the baseline.
- Added `run_tests` helper for reproducible test runs.
- Added `.gitignore` to exclude venv and temporary artifacts.

## Performance report 🧪

The benchmark produces `artifacts/perf_report.json` when running `run_benchmark()` (called by the test suite).

Measured results from a sample run (stored in `artifacts/perf_report.json`):

| metric | value |
|---|---:|
| **baseline_time_s** | 26.0519289 |
| **optimized_time_s** | 0.0394378 |
| **speedup** | 660.58 |
| **baseline_rss_mb** | 32.988 |
| **optimized_rss_mb** | 32.992 |

These numbers show the optimized implementation meets the project targets (optimized_time_s <= 0.35 and speedup >= 12).

You can re-run the benchmark manually with:

```bash
python -c "from fuzzbench.benchmark import run_benchmark; print(run_benchmark())"
```

## Notes on correctness and optimization 💡

- Correctness: The optimized implementation computes the same score formula as the baseline (1 - levenshtein_distance / max_len) * 100.0, ensuring numerical parity within floating point tolerance.
- Performance: The baseline implemented Levenshtein in Python (O(L^2) per pair in Python), while the optimized version delegates distance computation to `rapidfuzz` which is implemented in C and significantly faster. This eliminates the Python-level quadratic inner loops as the heavy work runs in native code.

## Reproducibility

- Dependencies are pinned in `requirements.txt`.
- Re-running `./run_tests` after deleting `.venv` will recreate the environment and re-run tests.
