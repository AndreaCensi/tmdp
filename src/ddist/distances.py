from contracts import contract

import numpy as np

from .ddist_contracts import *


__all__ = [
    'ddist_diff_l1',
]

@contract(d1='ddist', d2='ddist', returns='float, >=0')
def ddist_diff_l1(d1, d2):
    """ L1 difference between distributions. """
    all_states = set(d1) | set(d2)
    diff = 0.0
    for s in all_states:
        diff += np.abs(d1.get(s, 0) - d2.get(s, 0))
    return diff
