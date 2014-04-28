from collections import defaultdict

from contracts import contract
from .slice_sampling import slice_sampler


__all__ = [
    'ddist_evolve',
    'ddist_sample',
]

@contract(d='ddist', cond='cond_ddist', returns='ddist')
def ddist_evolve(d, cond):
    """ Evolves one distribution d according to the conditional distribution cond. """

    res = defaultdict(lambda: 0.0)
    for s, p_s in d.items():
        for s2, p_s2 in cond[s].items():
            p = p_s * p_s2
            if p > 0:
                res[s2] += p

    return dict(**res)


def ddist_sample(d):
    values = []
    probs = []
    for value, prob in d.items():
        values.append(value)
        probs.append(prob)

    #     assert sum(probs) == 1

    res = slice_sampler(probs, N=1)
    r = values[res]
    assert r in d
    return r
