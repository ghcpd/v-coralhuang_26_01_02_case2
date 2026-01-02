from typing import List
import concurrent.futures
from rapidfuzz.distance import Levenshtein
from .baseline_impl import Match


def ratio(a: str, b: str) -> float:
    if not a and not b:
        return 100.0
    m = max(len(a), len(b))
    return (1.0 - Levenshtein.distance(a, b) / m) * 100.0


def batch_best_match(queries: List[str], choices: List[str]) -> List[Match]:
    if not choices:
        return [Match("", -1.0) for _ in queries]

    def best_match(q):
        best_c, best_s = "", -1.0
        for c in choices:
            s = ratio(q, c)
            if s > best_s:
                best_c, best_s = c, s
        return Match(best_c, best_s)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        return list(executor.map(best_match, queries))
