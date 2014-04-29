from fractions import Fraction
import itertools

from contracts import contract

from gridmaps.map import GridMap
from gridworld.constants import GridWorldsConstants
from gridworld.grid_world import GridGeometry
from memos import memoize_instance
import numpy as np
from reprep.utils.frozen import frozendict2
from tmdp.configuration import get_conftools_tmdp_gridmaps
from tmdp.mdp import SimplePOMDP
from _collections import defaultdict
from gridworld.drawing import display_state_dist_only


__all__ = [
           'IntruderPOMDP',
]


class IntruderPOMDP(SimplePOMDP):
    undetected = 'U'

    @contract(gridmap='str|code_spec')
    def __init__(self, gridmap):
        _, self.gridmap = get_conftools_tmdp_gridmaps().instance_smarter(gridmap)
        assert isinstance(self.gridmap, GridMap)
        self._grid = GridGeometry(self.gridmap.get_obstacle_grid())

        intruders = self.gridmap.get_intruder_cells()

        if len(intruders) <= 1:
            raise ValueError('Not enough intruder cells')

        starts = self.gridmap.get_start_cells()

        if len(starts) == 0:
            raise ValueError('Not enough start cells')

        wrong = False
        for start, intruder in itertools.product(starts, intruders):
            if self._can_see(start, intruder):
                print('Start point %s can see intruder cell %s' % (start, intruder))

                obs = self.gridmap.get_obstacle_grid()
                for x in _trace_path(start, intruder):
                    obs[x] = '2'
                    print(x)
                obs[start] = '3'
                obs[intruder] = '3'
                print(obs)

                wrong = True

        if wrong:
            raise ValueError()

    def is_state(self, state):
        """ States are two tuples of two-coordinates (agent and intruder). """
        assert isinstance(state, tuple)
        assert len(state) == 2
        assert isinstance(state[0], tuple)
        assert isinstance(state[1], tuple)
        assert len(state[0]) == 2
        assert len(state[1]) == 2

    @memoize_instance
    def states(self):
        empty_cells = list(self.gridmap.get_empty_cells())
        intruder_cells = list(self.gridmap.get_intruder_cells())
        return list(itertools.product(empty_cells, intruder_cells))

    @memoize_instance
    def actions(self, state):
        robot, intruder = state  # @UnusedVariable
        actions = []
        for action, motion in GridWorldsConstants.action_to_displ.items():
            actions.append(action)
#             s2 = self._grid.next_cell(robot, motion)
#             if self._grid.is_empty(s2):
#                 actions.append(action)
        return actions

    @memoize_instance
    def transition(self, state, action):
        robot, intruder = state  # @UnusedVariable
        assert action in self.actions(state), '%s not in %s' % (action, self.actions(state))

        motion = GridWorldsConstants.action_to_displ[action]
        s2 = self._grid.next_cell(robot, motion)
        if self._grid.is_empty(s2):
            return {(s2, intruder): 1}
        else:
            return {(robot, intruder): 1}

    @memoize_instance
    def reward(self, state, action, state2):  # @UnusedVariable
        (di, dj) = GridWorldsConstants.action_to_displ[action]
        length = np.hypot(di, dj)
        return -length
        # TODO: add penalty for bumping?

    @memoize_instance
    def get_start_dist(self):
        raise NotImplemented
        start_cells = self.gridmap.get_start_cells()
        intruder_cells = self.gridmap.get_intruder_cells()

        states = list(itertools.product(start_cells, intruder_cells))
        d = {}
        for s in states:
            d[s] = 1.0 / len(states)
        return d


    @memoize_instance
    def is_goal_belief(self, belief):
        # We are done when we found it
        return len(belief) == 1

    @memoize_instance
    def get_observations(self):
        """ Observations of this POMDP are """
        # return [IntruderPOMDP.undetected] + self.gridmap.get_intruder_cells()
        empty_cells = list(self.gridmap.get_empty_cells())
        sensor = [IntruderPOMDP.undetected] + self.gridmap.get_intruder_cells()
        return list(itertools.product(empty_cells, sensor))

    @memoize_instance
    def get_observations_dist(self, state):
        robot, intruder = state  # @UnusedVariable
        # this is where the intruder can be
        # possibilities = self.gridmap.get_intruder_cells()
        #robot_can_see = which_can_see(self.grid_map, robot, possibilities)
        
        # Actually we have a deterministic 
        if self._can_see(robot, intruder):
            return {(robot, intruder): 1}
        else:
            return {(robot, IntruderPOMDP.undetected): 1}

    def _can_see(self, robot, intruder):
        trace = _trace_path(robot, intruder)
        obstacles = self.gridmap.get_wall_cells()
        occluded = set(trace) & set(obstacles)
        return not bool(occluded)

    def display_state_dist(self, pylab, state_dist):
        from gridworld.grid2 import GridWorld2

        dist_robot, dist_intruder = _get_marginals(state_dist)
        gw = GridWorld2(gridmap=self.gridmap)
        gw.display_state_dist(pylab, dist_robot)

        display_state_dist_only(pylab, dist_intruder, c1=[.8, .8, .8], c2=[0, 0, 1], ec='blue')

    def display_state_values(self, pylab, state_values):
        pass

    def display_policy(self, pylab, det_policy):
        pass

    @memoize_instance
    def get_start_dist_dist(self):
        """ Returns a distribution over distribution over states. """
        # for each possible start
        d = {}
        starts = self.gridmap.get_start_cells()
        for start in starts:
            intruder_cells = self.gridmap.get_intruder_cells()
            p = {}
            for intruder in intruder_cells:
                # p[(start, intruder)] = 1.0 / len(intruder_cells)
                p[(start, intruder)] = Fraction(1, len(intruder_cells))
            p = frozendict2(p)
            # d[p] = 1.0 / len(starts)
            d[p] = Fraction(1, len(starts))
        return d

    @memoize_instance
    def likelihood(self, state, observations):
        p = self.get_observations_dist(state=state)
        if not observations in p:
            return 0
#             msg = 'Tried to compute p(y|x) where:\n\ty = %s\n\tx = %s ' % (observations, state)
#             msg += '\nBut p(y|x) is:\n\t%s ' % p
#             raise ValueError(msg)
        return p[observations]

    def inference(self, belief, observations, use_fraction=False):
        belief2 = dict()
        p_y = self.partition(observations=observations, state_dist=belief,
                             use_fraction=use_fraction)
        if p_y == 0:
            msg = 'Tried to compute inference of p(x) given y but y cannot be generated by any x in p(x)'
#             msg += '\nBut p(y|x) is:\n\t%s ' % p
#
            raise SimplePOMDP.ObsNotPossible(msg)
        for x, p_x in belief.items():
            p_y_given_x = self.likelihood(observations=observations, state=x)
            p2 = p_x * p_y_given_x / p_y
            if p2 > 0:
                belief2[x] = p2

        belief2 = frozendict2(belief2.items())

        s = sum(belief2.values())
        if not s == 1.0:
            msg = 'Expected %s, got %s. ' % (1.0, s)
            msg += '\n %s' % belief2
            raise Exception(msg)
        return belief2

    def partition(self, state_dist, observations, use_fraction=False):
        if use_fraction:
            p = Fraction(0)
        else:
            p = 0.0
        # p(y) = p(y|x) * p(x)
        for state, p_state in state_dist.items():
            p += p_state * self.likelihood(state=state, observations=observations)
        return p

def _trace_path(a, b):
    a = np.array(a) * 1.0
    b = np.array(b) * 1.0
    n = np.max(np.abs(a - b))
    n = n * 3
    ps = []
    for alpha in np.linspace(0.0, 1.0, n):
        p = np.round(a * alpha + (1 - alpha) * b)
        p = (int(p[0]), int(p[1]))
        if not ps or ps[-1] != p:
            ps.append(p)
    return list(ps)




def _get_marginals(state_dist):
    dist_robot = defaultdict(lambda:0)
    dist_intruder = defaultdict(lambda:0)

    for (r, i), p in state_dist.items():
        dist_robot[r] += p
        dist_intruder[i] += p

    return frozendict2(dist_robot), frozendict2(dist_intruder)
