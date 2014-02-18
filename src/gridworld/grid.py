from itertools import product

from contracts import contract

from .constants import GridWorldsConstants
from .drawing import (display_policy, display_state_values,
    display_state_dist)
import numpy as np
from tmdp import SimpleMDP


__all__ = ['GridWorld']


class GridWorld(SimpleMDP):

    @contract(map='array[HxW](int,(=0|=1))')
    def __init__(self, map, goal, fail=0.3):  # @ReservedAssignment
        self._map = map
        self._goal = goal
        self._fail = fail

    def get_goal(self):
        return self._goal

    def get_map(self):
        return self._map

    def states(self):
        H, W = self._map.shape
        for (i,j) in product(range(H), range(W)):
            if self.is_empty((i,j)):
                yield (i, j)

    @contract(state='tuple(int,int)')
    def is_state(self, state):
        pass

    def is_empty(self, cell):
        return self._map[cell] == GridWorldsConstants.Empty

    def actions(self, state):  # @UnusedVariable
        return list(GridWorldsConstants.action_to_displ.keys())

    def _next_cell(self, state, action):
        i, j = state
        (di, dj) = GridWorldsConstants.action_to_displ[action]
        s2 = (i + di, j + dj)
        return s2

    def transition(self, state, action):
        # Goal is absorbing state
        if state == self._goal:
            return {self._goal: 1.0}

        s2 = self._next_cell(state, action)
        p = {}
        if self.is_empty(s2):
            p[state] = self._fail
            p[s2] = 1 - self._fail
        else:
            p[state] = 1
        return p

    def reward(self, state, action, state2):  # @UnusedVariable
        if state == self._goal:
            return 0.0
        else:
            if state == state2:  # bumped into wall
                return -2

            (di, dj) = GridWorldsConstants.action_to_displ[action]
            length = np.hypot(di, dj)
            return -length
        # return -1

    def display_policy(self, pylab, det_policy):
        display_policy(self, pylab, det_policy)

    def display_state_values(self, pylab, state_values):
        display_state_values(self, pylab, state_values)

    def display_state_dist(self, pylab, state_dist):
        display_state_dist(self, pylab, state_dist)
