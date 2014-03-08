import itertools

from contracts import contract

import numpy as np


__all__ = ['GridMap']

class GridMap():
    
    W = 1  # wall
    E = 0  # empty
    I = 2  # possible intruder
    S = 3  # start
    G = 4  # goal

    @contract(blocks='list[>=3](list[>=3](int))')
    def __init__(self, blocks):
        self.grid = np.flipud(blocks).T

    def get_wall_cells(self):
        """ Returns a list of coordinates where there is a wall. """
        return list(self._get_cells(values=[GridMap.W]))

    def get_empty_cells(self):
        """ Returns a list of coordinates where there is empty, I, Goal. """
        return list(self._get_cells(values=[GridMap.E, GridMap.I, GridMap.S, GridMap.G]))

    def get_goal_cells(self):
        """ Returns a list of coordinates where there is empty, I, Goal. """
        return list(self._get_cells(values=[GridMap.G]))

    def get_start_cells(self):
        """ Returns a list of coordinates for starting. """
        return list(self._get_cells(values=[GridMap.S]))

    def get_intruder_cells(self):
        """ Returns a list of coordinates for intruder """
        return list(self._get_cells(values=[GridMap.I]))

    def _get_cells(self, values):
        for i, j in iterate_indices(self.grid.shape):
            if self.grid[(i, j)] in values:
                yield (i, j)

    def get_obstacle_grid(self):
        """ Return np array with 1 for obstacles. """
        obs = (self.grid == GridMap.W) * 1.0
        return obs


def iterate_indices(shape):
    if len(shape) == 2:
        for i, j in itertools.product(range(shape[0]), range(shape[1])):
            yield i, j
    else:
        raise NotImplementedError
        assert(False)
