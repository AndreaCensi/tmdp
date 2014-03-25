from itertools import product

from contracts import contract

from gridworld.constants import GridWorldsConstants
import numpy as np


__all__ = ['GridGeometry']


class GridGeometry():
    
    @contract(grid='array')
    def __init__(self, grid):
        assert isinstance(grid, np.ndarray), type(grid)
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

    def is_occupied_float(self, x):
        cell = np.floor(x)
        cell = (int(cell[0]), int(cell[1]))
        return not self.is_empty(cell)

    def get_wall_corners(self):
        corners = set()
        def get_corners(P):
            return [(P[0], P[1]),
                    (P[0] + 1, P[1]),
                    (P[0] + 1, P[1] + 1),
                    (P[0], P[1] + 1)]

        def add_corner_between(P1, P2):
            d0 = P1[0] - P2[0]
            d1 = P1[1] - P2[1]
            assert np.abs(d0) == 1
            assert np.abs(d1) == 1
            common = list(set(get_corners(P1)) & set(get_corners(P2)))
            assert len(common) == 1
            corner = common[0]
            print('adding %s %s -> %s ' % (P1, P2, common))

            corners.add(corner)

        H, W = self._map.shape
        for (i, j) in product(range(1,H-1), range(1,W-1)):
            if not self.is_empty((i, j)):
                continue

            pA = (i - 1, j - 1)
            pB = (i - 1, j)
            pC = (i - 1, j + 1)
            pD = (i , j - 1)
            pF = (i, j + 1)
            pG = (i + 1, j - 1)
            pH = (i + 1, j)
            pI = (i + 1, j + 1)
            # ABC
            # DEF
            # GHI

            # AB
            # D
            # or
            # A0
            # 0

            def check_corner(P, n1, n2):
                wP = not(self.is_empty(P))
                w1 = not(self.is_empty(n1))
                w2 = not(self.is_empty(n2))
                
                if((wP & w1 & w2) or (wP & (not(w1)) & (not(w2)))):
                    add_corner_between((i, j), P)

            check_corner(pA, pB, pD)
            check_corner(pC, pB, pF)
            check_corner(pI, pF, pH)
            check_corner(pG, pD, pH)

            # ABC
            #   F
    
        return list(corners)
