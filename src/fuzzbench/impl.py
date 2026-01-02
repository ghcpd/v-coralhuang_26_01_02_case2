from typing import List
from .baseline_impl import Match
from rapidfuzz.distance import Levenshtein


def _ratio(a: str, b: str) -> float:
    """Match the baseline ratio implementation exactly.

    baseline: (1 - levenshtein_distance / max_len) * 100.0
    """
    if not a and not b:
        return 100.0
    m = max(len(a), len(b))
    # Levenshtein.distance from rapidfuzz is implemented in C and returns an int
    d = Levenshtein.distance(a, b)
    return (1.0 - d / m) * 100.0


def batch_best_match(queries: List[str], choices: List[str]) -> List[Match]:
    out: List[Match] = []
    # localize for speed
    _choices = choices
    _ratio_fn = _ratio

    for q in queries:
        best_c, best_s = "", -1.0
        for c in _choices:
            s = _ratio_fn(q, c)
            if s > best_s:
                best_c, best_s = c, s
        out.append(Match(best_c, best_s))
    return out
