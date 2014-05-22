from collections import defaultdict
from fractions import Fraction
import itertools

from contracts import contract

from gridmaps.map import GridMap
from gridworld.constants import GridWorldsConstants
from gridworld.drawing import display_state_dist_only
from gridworld.grid_world import GridGeometry
from memos import memoize_instance
import numpy as np
from reprep.utils.frozen import frozendict2
from tmdp.configuration import get_conftools_tmdp_gridmaps
from tmdp.mdp import SimplePOMDP
from gridmaps.raytracing import lineofsight


__all__ = [
     'IntruderPOMDPDec',
]


class IntruderPOMDPDec(SimplePOMDP):
    # Observation meaning that no intruder was detected
    undetected = 'U'

    @contract(gridmap='str|code_spec')
    def __init__(self, gridmap):
        _, self.gridmap = \
            get_conftools_tmdp_gridmaps().instance_smarter(gridmap)
        assert isinstance(self.gridmap, GridMap)
        self._grid = GridGeometry(self.gridmap.get_obstacle_grid())

        intruders = self.gridmap.get_intruder_cells()

        if len(intruders) <= 1:
            raise ValueError('Not enough intruder cells')

        starts = self.gridmap.get_start_cells()

        if len(starts) == 0:
            raise ValueError('Not enough start cells')

        check_can_see_from_start = False
        if check_can_see_from_start:
            wrong = False
            for start, intruder in itertools.product(starts, intruders):
                if self._can_see(start, intruder):
                    print('Start point %s can see intruder cell %s'
                          % (start, intruder))

                    obs = self.gridmap.get_obstacle_grid()
                    for x in _trace_path(start, intruder):
                        obs[x] = '2'
                        print(x)
                    obs[start] = '3'
                    obs[intruder] = '3'
                    print(obs)

                    wrong = True

            if wrong:
                raise ValueError('Agent can see intruder from start.')

    def get_gridmap(self):
        return self.gridmap

    def is_state(self, state):
        """ States are two tuples of two-coordinates (agent and intruder). """
        assert isinstance(state, tuple)
        assert len(state) == 2
        assert isinstance(state[0], tuple), state
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
        actions = []
        self.declare_actions = {}
        for intruder in self.gridmap.get_intruder_cells():
            dec = 'D-%s-%s' % intruder
            self.declare_actions[dec] = intruder
            actions.append(dec)


        robot, intruder = state  # @UnusedVariable

        for action, motion in GridWorldsConstants.action_to_displ.items():
            length = np.hypot(motion[0], motion[1])
            if length <= 1:
                actions.append(action)

        return actions


    @memoize_instance
    def is_goal_belief(self, belief):
        # We are done when we found it
        return len(belief) == 1  # and list(belief)[0] == self.found

    @memoize_instance
    def transition(self, state, action):
        robot, intruder = state  # @UnusedVariable
        assert action in self.actions(state), \
            '%s not in %s' % (action, self.actions(state))

        if action in self.declare_actions:
            return {state: 1}
        else:
            motion = GridWorldsConstants.action_to_displ[action]
            s2 = self._grid.next_cell(robot, motion)
            if self._grid.is_empty(s2):
                return {(s2, intruder): 1}
            else:
                return {(robot, intruder): 1}

    @memoize_instance
    def reward(self, state, action, state2):  # @UnusedVariable
        if action in self.declare_actions:
            declared = self.declare_actions[action]
            robot, intruder = state2  # @UnusedVariable
            if intruder == declared:
                return 0
            else:
                return -100
        else:
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
    def get_observations(self):
        """ Observations of this POMDP are """
        empty_cells = list(self.gridmap.get_empty_cells())
        sensor = ([IntruderPOMDPDec.undetected]
                  + self.gridmap.get_intruder_cells())
        return list(itertools.product(empty_cells, sensor))

    @memoize_instance
    def get_observations_dist(self, state):

        robot, intruder = state  # @UnusedVariable
        # this is where the intruder can be
        # possibilities = self.gridmap.get_intruder_cells()
        # robot_can_see = which_can_see(self.grid_map, robot, possibilities)

        # Actually we have a deterministic
        if self._can_see(robot, intruder):
            return {(robot, intruder): 1}
        else:
            return {(robot, IntruderPOMDPDec.undetected): 1}

    @memoize_instance
    def _can_see(self, robot, intruder):
        return lineofsight(self.gridmap, robot, intruder)

    def display_state_dist(self, pylab, state_dist):
        from gridworld.grid2 import GridWorld2

        dist_robot, dist_intruder = _get_marginals(state_dist)
        gw = GridWorld2(gridmap=self.gridmap)
        gw.display_state_dist(pylab, dist_robot)

        if len(dist_robot) == 1:
            # if there is only one state, display the rays
            robot = list(dist_robot)[0]
            self.display_robot_observations(pylab, robot)

        display_state_dist_only(pylab, dist_intruder,
                                c1=[.8, .8, .8], c2=[0, 0, 1], ec='blue')

    def display_robot_observations(self, pylab, robot):
        """ There is only one state for the robot so display the observations. """
        empty_cells = list(self.gridmap.get_empty_cells())
        seen = [cell
                for cell in empty_cells
                if self._can_see(robot, cell)]
        for cell in seen:
            p0 = np.array(robot) + np.array([0.5, 0.5])
            p1 = np.array(cell) + np.array([0.5, 0.5])
            pylab.plot([p0[0], p1[0]], [p0[1], p1[1]], 'y-')

    def get_grid_shape(self):
        return self._grid.get_map().shape

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
    
    
    def transition_back(self, state2, action):
        self.actions(state2)  # XXX init declare_action in init
        if action in self.declare_actions:
            return state2

        robot2, intruder = state2  # @UnusedVariable

        motion = GridWorldsConstants.action_to_displ[action]
        s = self._grid.next_cell(robot2, (-motion[0], -motion[1]))
        assert self._grid.is_empty(s)
        return (s, intruder)

    def evolve_back(self, state2_dist, action):
        state_dist = {}
        for state2, p in state2_dist.items():
            state = self.transition_back(state2, action)
            state_dist[state] = p
        return frozendict2(state_dist)

def _trace_path(a, b):
    a = np.array(a) * 1.0 + np.array([0.5, 0.5])
    b = np.array(b) * 1.0 + np.array([0.5, 0.5])
    n = np.max(np.abs(a - b))
    n = n * 3
    ps = []
    for alpha in np.linspace(0.0, 1.0, n):
        p = np.floor(a * alpha + (1 - alpha) * b)
        p = (int(p[0]), int(p[1]))
        if not ps or ps[-1] != p:
            ps.append(p)
    return list(ps)

def _trace_path_old(a, b):
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
