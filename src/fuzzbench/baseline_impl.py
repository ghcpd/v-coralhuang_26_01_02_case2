from dataclasses import dataclass
from typing import List


def levenshtein_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i]
        for j, cb in enumerate(b, start=1):
            cur.append(min(
                cur[j - 1] + 1,
                prev[j] + 1,
                prev[j - 1] + (ca != cb),
            ))
        prev = cur
    return prev[-1]


def ratio(a: str, b: str) -> float:
    if not a and not b:
        return 100.0
    m = max(len(a), len(b))
    return (1.0 - levenshtein_distance(a, b) / m) * 100.0


@dataclass(frozen=True)
class Match:
    choice: str
    score: float


def batch_best_match(queries: List[str], choices: List[str]) -> List[Match]:
    out = []
    for q in queries:
        best_c, best_s = "", -1.0
        for c in choices:
            s = ratio(q, c)
            if s > best_s:
                best_c, best_s = c, s
        out.append(Match(best_c, best_s))
    return out
