from contracts import contract

from .constants import GridWorldsConstants
from .grid_world import GridGeometry
from tmdp import SimpleMDP


class GenericGridWorld(SimpleMDP):
    """ This implements basic stuff, but not motion/obs models. """

    @contract(grid='array', goal='list', start='dict')
    def __init__(self, grid, goal, start):
        self.is_state_dist(start)
        self.is_state_set(goal)

        self._grid = GridGeometry(grid)
        self._goal = goal
        self._start = start
        
    def get_start_dist(self):
        return self._start

    def get_goal(self):
        return self._goal

    @contract(state='tuple(int,int)')
    def is_state(self, state):
        assert isinstance(state, tuple)
        assert len(state) == 2

    def states(self):
        return self._grid.get_empty_cells()

    def display_policy(self, pylab, det_policy):
        def a_to_motion(a):
            return GridWorldsConstants.action_to_displ[a]

        from gridworld.drawing import display_policy
        display_policy(grid=self._grid, goal=self.get_goal(),
                       pylab=pylab, policy=det_policy, a_to_motion=a_to_motion)

    def display_state_values(self, pylab, state_values):
        from gridworld.drawing import display_state_values
        display_state_values(grid=self._grid, goal=self.get_goal(),
                             pylab=pylab, state_values=state_values)

    def display_state_dist(self, pylab, state_dist):
        from gridworld.drawing import display_state_dist
        display_state_dist(grid=self._grid, goal=self.get_goal(),
                           pylab=pylab, state_dist=state_dist)
