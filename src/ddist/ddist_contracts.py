from contracts import new_contract
from numpy.testing.utils import assert_allclose


@new_contract
def ddist(dist):
    """ Makes sure dist is a distribution. """
    if len(dist) == 0:
        raise ValueError('Empty distribution.')
    values = dist.values()
    s = float(sum(values))

    assert_allclose(s, 1.0, err_msg='%s != 1.0' % s)


@new_contract
def cond_ddist(cond):
    """ conditional distribution. """
    if len(cond) == 0:
        raise ValueError('Empty conditional distribution.')

    for s, given_s in cond.items():
        ddist(given_s)
        # TODO: check domains


