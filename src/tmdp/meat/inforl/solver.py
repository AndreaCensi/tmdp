import numpy as np
from tmdp.mdp_utils.mdps_utils import all_actions
from .meat import inforl
from tmdp.meat.free_energy.report import report_free_energy
from tmdp.solver import SimpleMDPSolver


__all__ = ['INFORL']


class INFORL(SimpleMDPSolver):

    def __init__(self, beta, max_iterations, use_mdp_guess, z_diff_threshold):
        self.beta = beta
        self.max_iterations = max_iterations
        self.use_mdp_guess = use_mdp_guess
        self.z_diff_threshold = z_diff_threshold

    def solve(self, mdp):
        inforl_res = inforl(mdp=mdp,
                            use_mdp_guess=self.use_mdp_guess,
                            min_iterations=20,
                              max_iterations=self.max_iterations,
                              beta=self.beta,
                              z_diff_threshold=self.z_diff_threshold)
        inforl_res['iterations'] = select_some(inforl_res['iterations'],
                                               keep_initial=20,
                                               then_every=20)
        policy = inforl_res['iterations'][-1]['pi']

        res = {}
        res['inforl_res'] = inforl_res
        res['policy'] = policy
        return res


    def publish(self, r, mdp, result):  # @UnusedVariable
        report_free_energy(r, mdp, result['inforl_res'])

        its = result['inforl_res']['iterations']
        actions = list(all_actions(mdp))
        print 'actions', actions

        f = r.figure()

#         with f.plot('pi_hat') as pylab:
#             for action in actions:
#                 x = [it['pi_hat'][action] for it in its]
#                 pylab.plot(x, '.', label=action)

        with f.plot('median_F') as pylab:
            x = []
            for it in its:
                F = it['F']
                median = np.median([F[s] for s in F])
                x.append(median)
            pylab.plot(x)

        with f.plot('median_Z') as pylab:
            x = []
            for it in its:
                Z = it['Z']
                median = np.median([Z[s] for s in Z])
                x.append(median)
            pylab.plot(x)

        f = r.figure('policies')
        for i in [0, 1, 2, 10, 15, 20, 25, 30]:
            if i < len(its):
                policy = its[i]['pi']
                with f.plot('it%04d' % i) as pylab:
                    mdp.display_policy(pylab, policy)


def select_some(x, keep_initial=20, then_every=20):
    if len(x) <= keep_initial + 1:
        return x

    initial = x[:keep_initial]
    assert len(initial) == keep_initial
    middle = x[keep_initial:then_every:-1]
    last = [x[-1]]
    return initial + middle + last





