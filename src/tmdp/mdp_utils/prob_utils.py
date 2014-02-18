from tmdp.mdp_utils.slice_sampling import slice_sampler

def sample_from_dist(p):
    values = []
    probs = []
    for value, prob in p.items():
        values.append(value)
        probs.append(prob)

    #     assert sum(probs) == 1

    res = slice_sampler(probs, N=1)
    r = values[res]
    assert r in p
    return r


def _uniform_dist(what):
    what = list(what)
    n = len(what)
    p = {}
    for s in what:
        p[s] = 1.0 / n
    return p
