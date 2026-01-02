from typing import List
from .baseline_impl import Match


def _levenshtein_distance_fast(a: str, b: str) -> int:
    """
    Fast Levenshtein distance using RapidFuzz's native C++ implementation.
    Falls back to pure Python implementation that matches the baseline exactly.
    """
    # Try using RapidFuzz's levenshtein if available for speed
    try:
        from rapidfuzz.distance import Levenshtein
        return Levenshtein.distance(a, b)
    except Exception:
        # Fallback to baseline implementation if RapidFuzz is not available
        pass
    
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


def batch_best_match(queries: List[str], choices: List[str]) -> List[Match]:
    """
    Fast batch best match using RapidFuzz's optimized Levenshtein distance.
    
    For each query, finds the choice with the highest similarity score.
    Uses the baseline's scoring formula: (1 - distance / max_len) * 100
    """
    out = []
    
    if not choices:
        # If no choices, return all matches with empty choice and score -1.0
        for q in queries:
            out.append(Match("", -1.0))
        return out
    
    for q in queries:
        best_c = choices[0]
        best_s = -1.0
        
        # Find best match among all choices
        for c in choices:
            # Use baseline's exact scoring formula
            if not q and not c:
                s = 100.0
            else:
                m = max(len(q), len(c))
                dist = _levenshtein_distance_fast(q, c)
                s = (1.0 - dist / m) * 100.0
            
            if s > best_s:
                best_c, best_s = c, s
        
        out.append(Match(best_c, best_s))
    
    return out
