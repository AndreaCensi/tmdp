from gridworld.constants import GridWorldsConstants
from gridworld.generic_grid_world import GenericGridWorld
import numpy as np

__all__ = ['GridWorld2']

class GridBump(GenericGridWorld):
    """ 
        In this version collisions are OK and incur a cost. 
    """

    def __init__(self, gridmap, diagonal_cost, bump_reward):  # @ReservedAssignment
        GenericGridWorld.__init__(self, gridmap=gridmap)

        self._diagonal_cost = diagonal_cost
        self._bump_reward = bump_reward

    def actions(self, state):  # @UnusedVariable
        return list(GridWorldsConstants.action_to_displ)

    def transition(self, state, action):
        assert action in self.actions(state), '%s not in %s' % (action, self.actions(state))
        # Goal is absorbing state
        if state in self._goal:
            return {state: 1.0}

        motion = GridWorldsConstants.action_to_displ[action]
        s2 = self._grid.next_cell(state, motion)
        if self._grid.is_empty(s2):
            return {s2: 1.0}
        else:
            return {state: 1.0}  # stay there

    def reward(self, state, action, state2):  # @UnusedVariable
        assert action in self.actions(state)

        if state in self._goal:
            return 0.0
        else:
            if state == state2:  # bumped into wall
                return self._bump_reward

            if self._diagonal_cost:
                (di, dj) = GridWorldsConstants.action_to_displ[action]
                length = np.hypot(di, dj)
                return -length
            else:
                return -1.0

