from contextlib import contextmanager
from itertools import product

from matplotlib.patches import Rectangle

import numpy as np
from gridworld.grid_world import GridGeometry
from contracts import contract


@contextmanager
@contract(grid=GridGeometry)
def _display_map(grid, goal, pylab):
    gridmap = grid.get_map()
    H, W = gridmap.shape
    a = pylab.gca()

    a.add_patch(Rectangle((0, 0), H, W, edgecolor='black'))

    gg = GridGeometry(gridmap)

    for (i, j) in product(range(H), range(W)):
        if gg.is_empty((i, j)):
            attrs = dict(fc='white', ec='black')
        else:
            attrs = dict(fc='black', ec='white')
        a.add_patch(Rectangle((i, j), 1, 1, **attrs))

    yield pylab

    for g in goal:
        a.add_patch(Rectangle(g, 1, 1, ec='blue', fc='none'))

    pylab.axis((-1, H + 1, -1, W + 1))
    pylab.axis('equal')


def _display_cell(pylab, state, **attrs):
    a = pylab.gca()
    i, j = state
    a.add_patch(Rectangle((i, j), 1, 1, **attrs))


@contract(grid=GridGeometry)
def _display_cell_action(grid, pylab, s, a, p_a):
    s2 = grid.next_cell(s, a)

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

@contract(grid=GridGeometry)
def display_policy(grid, goal, pylab, policy, a_to_motion):
    """ Displays a policy (map from states to P(actions)). 
        a_to_motion: maps actions to arrows
    """
    with _display_map(grid, goal, pylab):
        for s, prob_a in policy.items():
            for a, p_a in prob_a.items():
                motion = a_to_motion(a)
                _display_cell_action(grid, pylab, s, motion, p_a)


@contract(grid=GridGeometry)
def display_state_values(grid, goal, pylab, state_values):
    values = np.array(state_values.values())
    m = values.min()
    M = values.max()
    norm = lambda x: (x - m) / (M - m)

    with _display_map(grid, goal, pylab):
        for s, v in state_values.items():
            fc = [norm(v), norm(v), norm(v)]
            _display_cell(pylab, s, fc=fc)


@contract(grid=GridGeometry)
def display_state_dist(grid, goal, pylab, state_dist):
    with _display_map(grid, goal, pylab):
        max_p = max(state_dist.values())
        for (i, j), p  in state_dist.items():
            c1 = np.array([0.8, 0.8, 0.8])
            c2 = np.array([0.0, 1.0, 0.0])
            p = p / max_p
            color = c1 * (1 - p) + c2 * p
            _display_cell(pylab, (i, j), fc=color, ec='red')



