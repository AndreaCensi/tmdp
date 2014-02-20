from tmdp.meat.value_it.meat import (vit_solve, policy_from_value,
    policy_from_value_least_committed)
from tmdp.solver import SimpleMDPSolver


__all__ = ['VITMDPSolver']


class VITMDPSolver(SimpleMDPSolver):
    """ Solves an MDP using value iteration. """

    def __init__(self, least_committed=True):
        self.least_committed = least_committed

    def solve(self, mdp):
        value = vit_solve(mdp)
        if self.least_committed:
            policy = policy_from_value_least_committed(mdp, value)
        else:
            policy = policy_from_value(mdp, value)

        res = {}
        res['value'] = value
        res['policy'] = policy
        return res

    def publish(self, r, mdp, result):  # @UnusedVariable
        f = r.figure()
        value = result['value']
        with f.plot('value') as pylab:
            mdp.display_state_values(pylab, value)

