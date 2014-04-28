import numpy as np
from ddist.operations import ddist_sample

sample_from_dist = ddist_sample

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
