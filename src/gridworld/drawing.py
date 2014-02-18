from contextlib import contextmanager
from itertools import product

from matplotlib.patches import Rectangle

import numpy as np


@contextmanager
def _display_map(grid, pylab):
    goal = grid.get_goal()
    gridmap = grid.get_map()
    H, W = gridmap.shape
    a = pylab.gca()

    a.add_patch(Rectangle((0, 0), H, W, edgecolor='black'))

    for (i, j) in product(range(H), range(W)):
        if grid.is_empty((i, j)):
            attrs = dict(fc='white', ec='black')
        else:
            attrs = dict(fc='black', ec='white')
        a.add_patch(Rectangle((i, j), 1, 1, **attrs))

    yield pylab

    a.add_patch(Rectangle(goal, 1, 1, ec='blue', fc='none'))

    pylab.axis((-1, H + 1, -1, W + 1))
    pylab.axis('equal')

def _display_cell(pylab, state, **attrs):
    a = pylab.gca()
    i, j = state
    a.add_patch(Rectangle((i, j), 1, 1, **attrs))

def _display_cell_action(grid, pylab, s, a, p_a):
    s2 = grid._next_cell(s, a)

    if False:
        e = p_a * 0.9
        d0 = (s2[0] - s[0]) * e
        d1 = (s2[1] - s[1]) * e

        if e > 0.3:
            head_width = 0.15
        else:
            head_width = 0
        pylab.arrow(s[0] + 0.5, s[1] + 0.5, d0, d1, ec='black', lw=0.15,
                    shape='full', head_width=head_width, length_includes_head=True)
    else:
        e = p_a * 0.45
        d0 = (s2[0] - s[0]) * e
        d1 = (s2[1] - s[1]) * e

        if e > 0.01:
            head_width = 0
            pylab.arrow(s[0] + 0.5, s[1] + 0.5, d0, d1, ec='black', lw=0.15,
                        shape='full', head_width=head_width, length_includes_head=True)

def display_policy(grid, pylab, det_policy):
    """ Displays a policy (map from states to P(actions)). """
    with _display_map(grid, pylab):
        for s, prob_a in det_policy.items():
            for a, p_a in prob_a.items():
                _display_cell_action(grid, pylab, s, a, p_a)

def display_state_values(grid, pylab, state_values):
    values = np.array(state_values.values())
    m = values.min()
    M = values.max()
    norm = lambda x: (x - m) / (M - m)

    with _display_map(grid, pylab):
        for s, v in state_values.items():
            fc = [norm(v), norm(v), norm(v)]
            _display_cell(pylab, s, fc=fc)

def display_state_dist(grid, pylab, state_dist):
    with _display_map(grid, pylab):
        max_p = max(state_dist.values())
        for (i, j), p  in state_dist.items():
            c1 = np.array([0.8, 0.8, 0.8])
            c2 = np.array([0.0, 1.0, 0.0])
            p = p / max_p
            color = c1 * (1 - p) + c2 * p
            _display_cell(pylab, (i, j), fc=color, ec='red')
