from gridworld.grid import GridWorld
from gridworld.grid2 import GridWorld2
from gridworld.gridpo import POGridWorld
import numpy as np


class EmptyGrid5(GridWorld):

    def __init__(self):

        grid = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, ],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, ],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, ],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, ],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, ],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, ],
        ])
        print grid
        GridWorld.__init__(self, map=grid, goal=(4, 3))



class TishbyMaze(GridWorld):

    def __init__(self):
        W = 1
        E = 0
        G = E
        grid = np.array([
            [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, G, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, W, W, W, W, W, W, W, W, W, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, W, W, W, W, W, W, W, W, W, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        ])
        grid = np.flipud(grid.T)
        goal = (11, 11)
        GridWorld.__init__(self, map=grid, goal=goal, fail=0)



class TishbyMaze2(GridWorld2):

    def __init__(self, fail=0):
        W = 1
        E = 0
        G = E
        grid = np.array([
            [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, G, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, W, W, W, W, W, W, W, W, W, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, W, W, W, W, W, W, W, W, W, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        ])
        grid = np.flipud(grid.T)
        goal = (11, 11)
        GridWorld2.__init__(self, map=grid, goal=goal, fail=fail)


class POShape1(POGridWorld):
    def __init__(self, p_fail, p_loc, bump_reward=-10):
        grid, start, goal = get_shape1()
        POGridWorld.__init__(self, map=grid, p_fail=p_fail, p_loc=p_loc,
                             bump_reward=bump_reward, goal=goal, start=start)


def get_shape1():
    """ Returns grid, goal, start. """
    W = 1
    E = 0
    grid = np.array([
            [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, W, W, W, W, W, W, W, W, W, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
            [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        ])
    grid = np.flipud(grid).T


    start = {(7, 7): 1.0}
    goal = [(2, 2)]
    return grid, start, goal

