from tmdp.mdp_utils.slice_sampling import slice_sampler
import numpy as np

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

def _random_dist(what):
    what = list(what)
    # random probability distribution
    prob = np.random.rand(len(what))
    prob = prob / np.sum(prob)
    p = {}
    for i, s in enumerate(what):
        p[s] = prob[i]
    return p
