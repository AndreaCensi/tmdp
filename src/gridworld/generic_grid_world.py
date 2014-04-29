from contracts import contract

from gridmaps.map import GridMap
from gridworld.drawing import display_neigh_field_value, display_state_dist_only
from tmdp import SimpleMDP
from tmdp.configuration import get_conftools_tmdp_gridmaps
from tmdp.mdp_utils.prob_utils import _uniform_dist

from .constants import GridWorldsConstants
from .grid_world import GridGeometry


__all__ = ['GenericGridWorld']


class GenericGridWorld(SimpleMDP):
    """ This implements basic stuff, but not motion/obs models. """

    @contract(gridmap='str|code_spec')
    def __init__(self, gridmap):
    
        _, self.gridmap = get_conftools_tmdp_gridmaps().instance_smarter(gridmap)
        assert isinstance(self.gridmap, GridMap)
        self._grid = GridGeometry(self.gridmap.get_obstacle_grid())

        goal = self.gridmap.get_goal_cells()
        start = _uniform_dist(self.gridmap.get_start_cells())
        
        self.is_state_dist(start)
        self.is_state_set(goal)

        self._goal = goal
        self._start = start
        
    @contract(returns=GridGeometry)
    def get_grid(self):
        return self._grid

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

    def display_state_dist(self, pylab, state_dist, **kwargs):
        """ kwargs[c1,c2] = [r,g,b] """
        from gridworld.drawing import display_state_dist
        display_state_dist(grid=self._grid, goal=self.get_goal(),
                           pylab=pylab, state_dist=state_dist, **kwargs)



    def display_neigh_field_value(self, pylab, neig_values):
        display_neigh_field_value(self._grid, pylab, neig_values)


    def get_support_points(self):
        """ Returns a list of fundamental point to include in the sampling. """
        return self._grid.get_wall_corners()


