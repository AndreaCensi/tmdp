from grid_intruder.intruder_pomdp import IntruderPOMDP
from contracts import contract
from memos.memoization import memoize_instance
import itertools
import numpy as np
from reprep.utils.frozen import frozendict2
from matplotlib.patches import Rectangle
from gridmaps.raytracing import lineofsight

__all__ = [
     'IntruderPOMDPrf',
]


class IntruderPOMDPrf(IntruderPOMDP):
    """ This provides a range-finder like observation model. """
    EMPTY = 0
    OCCUPIED = 1
    OCCLUDED = 2
    status2color = {
        0: [1, 1, 1],
        1: [0, 0, 0],
        2: [.6, .6, .6]
    }
    @contract(horizon='int,>=1')
    def __init__(self, gridmap, horizon):
        IntruderPOMDP.__init__(self, gridmap=gridmap)
        self.horizon = horizon

    @memoize_instance
    def get_observations_dist(self, state):
        robot, intruder = state  # @UnusedVariable
        # use perfect sensor to detect
        _, intruder_detected = list(IntruderPOMDP.get_observations_dist(self, state))[0]
        
        rf = self.get_simulated_rangefinder(robot, horizon=self.horizon)
        z = (rf, intruder_detected)
        return frozendict2({z:1})

    @memoize_instance
    @contract(horizon='int,>=1,M')
    def get_simulated_rangefinder(self, robot, horizon):
#         robot, intruder = state  # @UnusedVariable
        dx = range(-horizon, horizon + 1)
        dy = range(-horizon, horizon + 1)
        assert dx[0] == -horizon
        assert dx[-1] == +horizon
#         res = {}
#         s = ""
        a = np.empty(shape=(horizon*2+1,horizon*2+1), dtype='int')
        for delta_x, delta_y in itertools.product(dx, dy):
            cell = (delta_x + robot[0], delta_y + robot[1])

            if not self._grid.is_inside(cell):
                value = IntruderPOMDPrf.OCCLUDED
            else:
                unoccluded = self._unoccluded(robot, cell)
                if unoccluded:
                    if self._grid.is_empty(cell):
                        value = IntruderPOMDPrf.EMPTY
                    else:
                        value = IntruderPOMDPrf.OCCUPIED
                else:
                    value = IntruderPOMDPrf.OCCLUDED
                
            c = (delta_x+horizon, delta_y+horizon)
            a[c] = value
#             s += '%d' % value
#             res[cell] = value
        res = tuple(map(tuple, a.tolist()))
        return res


    @memoize_instance
    def _unoccluded(self, cell1, cell2):
        """ No ostacles between cell1 and any corner of cell2. """
        return lineofsight(self.gridmap, cell1, cell2)
#
#         def center_of(c):
#             return np.array([c[0]+0.5, c[1]+0.5])
#         def corners_of(c):
#             c0 = np.array([c[0], c[1]], dtype='float')
#             c1 = c0 + [0,1]
#             c2 = c0 + [1,0]
#             c3 = c0 + [1,1]
#             return [c0,c1,c2,c3]
#
#         def unoccluded(p0, p1, c1,c2):
#             trace = set(my_trace_path(cell1, cell2))
#             if c1 in trace:
#                 trace.remove(c1)
#             if c2 in trace:
#                 trace.remove(c2)
#             obstacles = self.gridmap.get_wall_cells()
#             occluded = set(trace) & set(obstacles)
#             return not bool(occluded)
#         def my_trace_path(a, b):
#             a = np.array(a) * 1.0 + np.array([0.5, 0.5])
#             b = np.array(b) * 1.0 + np.array([0.5, 0.5])
#             n = np.max(np.abs(a - b))
#             n = n * 3
#             ps = []
#             for alpha in np.linspace(0.0, 1.0, n):
#                 p = np.floor(a * alpha + (1 - alpha) * b)
#                 p = (int(p[0]), int(p[1]))
#                 if not ps or ps[-1] != p:
#                     ps.append(p)
#             return list(ps)
#
#         u = [ unoccluded(center_of(cell1), p1, cell1, cell2)
#              for p1 in corners_of(cell2) ]
#         return np.any(u)







    def display_robot_observations(self, pylab, robot):
        horizon = self.horizon
        y = np.array(self.get_simulated_rangefinder(robot, self.horizon))
        dx = range(-horizon, horizon + 1)
        dy = range(-horizon, horizon + 1)

        a = pylab.gca()


        for delta_x, delta_y in itertools.product(dx, dy):
            cell = (delta_x + robot[0], delta_y + robot[1])
            if delta_x == 0 and delta_y == 0:
                continue
            if not self._grid.is_inside(cell):
                continue
            c = (delta_x + horizon, delta_y + horizon)
            value = y[c]
            color = IntruderPOMDPrf.status2color[value]
            W = 0.4
            p0 = np.array(cell) + np.array([0.5 - W / 2, 0.5 - W / 2])
            attrs = dict(fc=color)
            a.add_patch(Rectangle(p0, W, W, **attrs))



