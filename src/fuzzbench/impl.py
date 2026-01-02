from typing import List
from .baseline_impl import Match
from rapidfuzz.distance import Levenshtein


def _ratio_from_distance(a: str, b: str, d: int) -> float:
    """Compute ratio exactly like the baseline implementation.

    Baseline: (1 - levenshtein_distance / max(len(a), len(b))) * 100.0
    """
    if not a and not b:
        return 100.0
    m = max(len(a), len(b))
    return (1.0 - d / m) * 100.0


def batch_best_match(queries: List[str], choices: List[str]) -> List[Match]:
    out: List[Match] = []
    for q in queries:
        best_c = ""
        best_s = -1.0
        # Preserve baseline behavior when choices is empty
        for c in choices:
            d = Levenshtein.distance(q, c)
            s = _ratio_from_distance(q, c, d)
            if s > best_s:
                best_c, best_s = c, s
        out.append(Match(best_c, best_s))
    return out
