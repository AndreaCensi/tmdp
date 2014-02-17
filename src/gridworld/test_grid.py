from tmpd.testing import checks_mdp
from gridworld.grid import EmptyGrid5


def test_grid_empty1():

    empty = EmptyGrid5()

    checks_mdp(empty)
