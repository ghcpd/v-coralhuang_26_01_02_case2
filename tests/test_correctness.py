from fuzzbench import baseline_impl, impl


def test_consistency():
    queries = ["kitten", "flaw"]
    choices = ["kitchen", "bitten", "flaws"]
    b = baseline_impl.batch_best_match(queries, choices)
    o = impl.batch_best_match(queries, choices)

    assert [m.choice for m in o] == [m.choice for m in b]
    for x, y in zip(b, o):
        assert abs(x.score - y.score) < 1e-6
