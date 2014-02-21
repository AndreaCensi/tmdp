
from gridworld.constants import GridWorldsConstants
from tmdp.mdp_utils.prob_utils import _uniform_dist
from gridworld.grid2 import GridWorld2


__all__ = ['GridWorldReset']

class GridWorldReset(GridWorld2):
    """ 
        This is a version where the state is reset to a random state
        when it reaches the goal.
    """

    def transition(self, state, action):
        assert action in self.actions(state)
        # Goal is absorbing state
        if state in self._goal:
            return _uniform_dist(self.states())

        motion = GridWorldsConstants.action_to_displ[action]
        s2 = self._grid.next_cell(state, motion)
        assert  self._grid.is_empty(s2)

        return {s2: 1.0}

