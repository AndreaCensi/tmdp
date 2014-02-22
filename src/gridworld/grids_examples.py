# from gridworld.grid import GridWorld
from gridworld.grid2 import GridWorld2
from gridworld.gridpo import POGridWorld
import numpy as np
from gridworld.grid_world_reset import GridWorldReset

class TishbyMazeOrig(GridWorld2):

    def __init__(self, fail=0):
        grid, start, goal = get_maze1()
        GridWorld2.__init__(self, map=grid, goal=goal, fail=fail, diagonal_cost=False, start=start)

class RubinMazeOrig(GridWorld2):

    def __init__(self, fail=0):
        grid, start, goal = get_rubin_maze()
        GridWorld2.__init__(self, map=grid, goal=goal, fail=fail, diagonal_cost=False, start=start)

class RubinMazeDiag(GridWorld2):

    def __init__(self, fail=0):
        grid, start, goal = get_rubin_maze()
        GridWorld2.__init__(self, map=grid, goal=goal, fail=fail, diagonal_cost=True, start=start)

class TishbyMazeDiag(GridWorld2):
    """ Using diagonal cost """

    def __init__(self, fail=0):
        grid, start, goal = get_maze1()
        GridWorld2.__init__(self, map=grid, goal=goal, fail=fail, diagonal_cost=True, start=start)

class TishbyMazeReset(GridWorldReset):

    def __init__(self, fail=0):
        grid, start, goal = get_maze1()
        GridWorld2.__init__(self, map=grid, goal=goal, fail=fail, diagonal_cost=False, start=start)

class POMaze1(POGridWorld):
    def __init__(self, p_fail, p_loc, bump_reward=-10):
        grid, start, goal = get_maze1()
        POGridWorld.__init__(self, map=grid, p_fail=p_fail, p_loc=p_loc,
                             bump_reward=bump_reward, goal=goal, start=start)

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


    start = {(2, 10): 1.0}
    goal = [(2, 2)]
    return grid, start, goal

def get_maze1():
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
    grid = np.flipud(grid).T
    start = {(2, 2): 1.0}
    goal = [(11, 11)]
    return grid, start, goal




def get_rubin_maze():
    W = 1
    E = 0
    grid = np.array([
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ])
    grid = np.flipud(grid).T
    start = {(1, 10): 1.0}
    goal = [(11, 5)]
    return grid, start, goal


