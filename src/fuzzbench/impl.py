from typing import List
from .baseline_impl import Match

try:
    from rapidfuzz.distance import Levenshtein
except Exception as e:  # pragma: no cover - environment should provide rapidfuzz
    Levenshtein = None


def _compute_ratio(a: str, b: str) -> float:
    """Match the baseline_impl.ratio behavior exactly but use RapidFuzz's
    C implementation for the edit distance when available.
    """
    if not a and not b:
        return 100.0
    m = max(len(a), len(b))
    if m == 0:
        return 100.0
    if Levenshtein is None:
        # Fallback to a simple Python implementation if rapidfuzz missing.
        # This path is not expected in the test environment (rapidfuzz is pinned
        # in requirements), but keeps the behavior identical.
        from .baseline_impl import levenshtein_distance

        d = levenshtein_distance(a, b)
    else:
        # Use C implementation to get an integer edit distance (identical
        # semantics to the baseline integer distance) and compute the same
        # normalized ratio so floating results match closely.
        d = Levenshtein.distance(a, b)
    return (1.0 - (d / m)) * 100.0


def batch_best_match(queries: List[str], choices: List[str]) -> List[Match]:
    """Optimized implementation that is behaviorally identical to the
    baseline but uses RapidFuzz's C routines for the heavy work.

    Characteristics preserved from baseline:
    - If `choices` is empty returns Match("", -1.0) for each query
    - Tie-breaking: first occurrence in `choices` is chosen
    - Score computation matches baseline's formula exactly
    - Deterministic for identical inputs
    """
    out: List[Match] = []
    if not choices:
        # baseline returns "" and -1.0 when there are no choices
        return [Match("", -1.0) for _ in queries]

    # Localize for speed
    ratio_fn = _compute_ratio
    for q in queries:
        # baseline initial values
        best_c, best_s = "", -1.0
        # iterate choices in order to preserve tie-breaking behavior
        for c in choices:
            s = ratio_fn(q, c)
            if s > best_s:
                best_c, best_s = c, s
        out.append(Match(best_c, best_s))
    return out
