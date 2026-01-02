# fuzzbench — optimized batch matching

## How to run

- Create (or reuse) virtual environment and run tests:

  - Unix/macOS: ./run_tests
  - Windows PowerShell: .\run_tests.ps1

- Alternatively, install the pinned dependencies and run pytest:

  python -m venv .venv
  . .venv/bin/activate   # or .\.venv\Scripts\Activate.ps1 on Windows
  pip install -r requirements.txt
  pytest -q


## Performance summary

| metric | value |
|---|---:|
| baseline_time_s | 27.589609599999676 |
| optimized_time_s | 0.04321030000028259 |
| speedup | 638.4961363336807 |
| baseline_rss_mb | 32.99609375 |
| optimized_rss_mb | 32.99609375 |


## What was optimized

- Replaced the pure-Python Levenshtein implementation with RapidFuzz's C-backed
  Levenshtein distance for tight inner-loop computation.

Why it improves performance

- The baseline computes an O(L^2) dynamic-programming edit distance in Python
  for every pair; moving the distance computation into RapidFuzz's C implementation
  reduces per-comparison overhead dramatically and meets the required speedups.

How correctness is preserved

- The optimized code computes the exact same score as the baseline using
  Levenshtein distance and the identical normalization formula.


## Notes for reviewers

- The benchmark writes `artifacts/perf_report.json` with timing and RSS.
- The `tests/` directory enforces correctness and performance gates.
- See `src/fuzzbench/impl.py` for the optimized implementation.
