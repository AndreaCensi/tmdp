from itertools import product
from gridworld.constants import GridWorldsConstants
from contracts import contract

__all__ = ['GridGeometry']


class GridGeometry():
    
    def __init__(self, grid):
        self._map = grid

    def get_map(self):
        return self._map

    def get_empty_cells(self):
        H, W = self._map.shape
        for (i, j) in product(range(H), range(W)):
            if self.is_empty((i, j)):
                yield (i, j)

    @contract(cell='tuple(int,int)')
    def is_empty(self, cell):
        return self._map[cell] == GridWorldsConstants.Empty

    @contract(cell='tuple(int,int)', motion='tuple(int,int)')
    def next_cell(self, cell, motion):
        i, j = cell
        (di, dj) = motion  # GridWorldsConstants.action_to_displ[action]
        s2 = (i + di, j + dj)
        return s2
