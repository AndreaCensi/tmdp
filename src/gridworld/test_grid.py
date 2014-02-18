from gridworld.grid import EmptyGrid5
from tmpd.testing import checks_mdp


def test_grid_empty1():

    empty = EmptyGrid5()

    checks_mdp(empty)
