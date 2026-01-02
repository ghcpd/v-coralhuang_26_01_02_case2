from typing import List
from .baseline_impl import Match
from . import baseline_impl


def batch_best_match(queries: List[str], choices: List[str]) -> List[Match]:
    return baseline_impl.batch_best_match(queries, choices)
