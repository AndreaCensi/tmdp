from itertools import product

from contracts import contract
from matplotlib.patches import Rectangle

import numpy as np
from tmdp import SimpleMDP
from contextlib import contextmanager


__all__ = ['GridWorld2']


class GridWorld2(SimpleMDP):
    """ 
        This is a version of the grid world where collisions are not allowed
        as actions. 
    """
    Empty = 0
    Obstacle = 1
    action_to_displ = {
       'r': (-1, 0),
       'l': (+1, 0),
       'd': (0, -1),
       'u': (0, +1),
       'rd': (-1, -1),
       'ld': (+1, -1),
       'ru': (-1, +1),
       'lu': (+1, +1),
       }

    @contract(map='array[HxW](int,(=0|=1))')
    def __init__(self, map, goal, fail=0.3):  # @ReservedAssignment
        self._map = map
        self._goal = goal
        self._fail = fail

    def states(self):
        H, W = self._map.shape
        for (i, j) in product(range(H), range(W)):
            if self.is_empty((i, j)):
                yield (i, j)

    @contract(state='tuple(int,int)')
    def is_state(self, state):
        pass

    def is_empty(self, cell):
        return self._map[cell] == GridWorld2.Empty

    def actions(self, state):
        actions = []
        for action in self.action_to_displ:
            s2 = self._next_cell(state, action)
            if self.is_empty(s2):
                actions.append(action)
        return actions

    def _next_cell(self, state, action):
        i, j = state
        (di, dj) = GridWorld2.action_to_displ[action]
        s2 = (i + di, j + dj)
        return s2

    def transition(self, state, action):
        assert action in self.actions(state)
        # Goal is absorbing state
        if state == self._goal:
            return {self._goal: 1.0}

        s2 = self._next_cell(state, action)
        assert  self.is_empty(s2)

        return {s2: 1.0}

        if False:
            p = {}
            p[state] = self._fail
            p[s2] = 1 - self._fail
            return p

    def reward(self, state, action, state2):  # @UnusedVariable
        assert action in self.actions(state)

        if state == self._goal:
            return 0.0
        else:
            if state == state2:  # bumped into wall
                assert False, ('%s -> %s -> %s' % (state, action, state2))

            (di, dj) = GridWorld2.action_to_displ[action]
            length = np.hypot(di, dj)
            return -length
            # return -1

    @contextmanager
    def _display_map(self, pylab):
        H, W = self._map.shape
        a = pylab.gca()

        a.add_patch(Rectangle((0, 0), H, W, edgecolor='black'))

        for (i, j) in product(range(H), range(W)):
            if self.is_empty((i, j)):
                attrs = dict(fc='white', ec='black')
            else:
                attrs = dict(fc='black', ec='white')
            a.add_patch(Rectangle((i, j), 1, 1, **attrs))

        yield pylab

        a.add_patch(Rectangle(self._goal, 1, 1, ec='blue', fc='none'))

        pylab.axis((-1, H + 1, -1, W + 1))
        pylab.axis('equal')

    def _display_cell(self, pylab, state, **attrs):
        a = pylab.gca()
        i, j = state
        a.add_patch(Rectangle((i, j), 1, 1, **attrs))

    def _display_cell_action(self, pylab, s, a, p_a):
        s2 = self._next_cell(s, a)

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

    def display_policy(self, pylab, det_policy):
        """ Displays a policy (map from states to P(actions)). """
        with self._display_map(pylab):
            for s, prob_a in det_policy.items():
                for a, p_a in prob_a.items():
                    self._display_cell_action(pylab, s, a, p_a)

    def display_state_values(self, pylab, state_values):
        values = np.array(state_values.values())
        m = values.min()
        M = values.max()
        norm = lambda x: (x - m) / (M - m)

        with self._display_map(pylab):
            for s, v in state_values.items():
                fc = [norm(v), norm(v), norm(v)]
                self._display_cell(pylab, s, fc=fc)

    def display_state_dist(self, pylab, state_dist):
        with self._display_map(pylab):
            max_p = max(state_dist.values())
            for (i, j), p  in state_dist.items():
                c1 = np.array([0.8, 0.8, 0.8])
                c2 = np.array([0.0, 1.0, 0.0])
                p = p / max_p
                color = c1 * (1 - p) + c2 * p
                self._display_cell(pylab, (i, j), fc=color, ec='red')

