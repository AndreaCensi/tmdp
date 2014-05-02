# from gridworld.grid import GridWorld
from gridworld.grid2 import GridWorld2
from gridworld.grid_bump import GridBump
from gridworld.grid_world_reset import GridWorldReset


class TishbyMazeOrig(GridWorld2):

    def __init__(self, fail=0):
        GridWorld2.__init__(self, 'tmaze', fail=fail, diagonal_cost=False)

class TishbyMazeBump(GridBump):

    def __init__(self, bump_reward):
        GridBump.__init__(self, 'tmaze', bump_reward=bump_reward, diagonal_cost=False)

class TishbyMazeBumpD(GridBump):

    def __init__(self, bump_reward):
        GridBump.__init__(self, 'tmaze', bump_reward=bump_reward, diagonal_cost=True)


class RubinMazeOrig(GridWorld2):

    def __init__(self, fail=0):
        GridWorld2.__init__(self, 'rmaze', diagonal_cost=False, fail=fail)

class RubinMazeDiag(GridWorld2):

    def __init__(self, fail=0):
        GridWorld2.__init__(self, 'rmaze', diagonal_cost=True, fail=fail
                            )

class TishbyMazeDiag(GridWorld2):
    """ Using diagonal cost """

    def __init__(self, fail=0):
        GridWorld2.__init__(self, 'tmaze', diagonal_cost=True, fail=fail)

class TishbyMazeReset(GridWorldReset):

    def __init__(self, fail=0):
        GridWorld2.__init__(self, 'tmaze', fail=fail, diagonal_cost=False)

