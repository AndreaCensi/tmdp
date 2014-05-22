
import itertools

from contracts import contract
from matplotlib.patches import Rectangle

from grid_intruder import IntruderPOMDPDec
from gridmaps.raytracing import lineofsight
from memos import memoize_instance
import numpy as np
from reprep.utils import frozendict2


__all__ = [
     'IntruderPOMDPrf',
]


class IntruderPOMDPrf(IntruderPOMDPDec):
    """ This provides a range-finder like observation model. """
    EMPTY = 0
    OCCUPIED = 1
    OCCLUDED = 2
    status2color = {
        0: [1, 1, 1],
        1: [0, 0, 0],
        2: [.6, .6, .6]
    }
    @contract(horizon='int,>=0')
    def __init__(self, gridmap, horizon):
        IntruderPOMDPDec.__init__(self, gridmap=gridmap)
        self.horizon = horizon

    @memoize_instance
    def get_observations_dist(self, state):
        robot, intruder = state  # @UnusedVariable
        # use perfect sensor to detect
        _, intruder_detected = list(IntruderPOMDPDec.get_observations_dist(self, state))[0]
        
        rf = self.get_simulated_rangefinder(robot, horizon=self.horizon)
        z = (rf, intruder_detected)
        return frozendict2({z:1})

    @memoize_instance
    @contract(horizon='int,>=0,M')
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

            # don't draw unknown
            if IntruderPOMDPrf.OCCLUDED == value:
                continue

            color = IntruderPOMDPrf.status2color[value]
            W = 0.4
            p0 = np.array(cell) + np.array([0.5 - W / 2, 0.5 - W / 2])
            attrs = dict(fc=color)
            a.add_patch(Rectangle(p0, W, W, **attrs))

        # also display camera
        IntruderPOMDPDec.display_robot_observations(self, pylab, robot)

