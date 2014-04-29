from contracts import contract

from gridworld.constants import GridWorldsConstants
from gridworld.generic_grid_world import GenericGridWorld
import numpy as np


__all__ = [
    'GridWorld2',
]


class GridWorld2(GenericGridWorld):
    """ 
        This is a version of the grid world where collisions are not allowed
        as actions. 
    """
    @contract(gridmap='str|code_spec')
    def __init__(self, gridmap, diagonal_cost=False, fail=0.3):
        GenericGridWorld.__init__(self, gridmap=gridmap)
        self._diagonal_cost = diagonal_cost
        self._fail = fail

    def actions(self, state):
        actions = []
        for action, motion in GridWorldsConstants.action_to_displ.items():
            s2 = self._grid.next_cell(state, motion)
            if self._grid.is_empty(s2):
                actions.append(action)
        return actions


    def transition(self, state, action):
        assert action in self.actions(state), '%s not in %s' % (action, self.actions(state))
        # Goal is absorbing state
        if state in self._goal:
            return {state: 1.0}

        motion = GridWorldsConstants.action_to_displ[action]
        s2 = self._grid.next_cell(state, motion)
        assert  self._grid.is_empty(s2)

        return {s2: 1.0}

        if False:
            p = {}
            p[state] = self._fail
            p[s2] = 1 - self._fail
            return p

    def reward(self, state, action, state2):  # @UnusedVariable
        assert action in self.actions(state)

        if state in self._goal:
            return 0.0
        else:
            if state == state2:  # bumped into wall
                assert False, ('%s -> %s -> %s' % (state, action, state2))

            if self._diagonal_cost:
                (di, dj) = GridWorldsConstants.action_to_displ[action]
                length = np.hypot(di, dj)
                return -length
            else:
                return -1.0

