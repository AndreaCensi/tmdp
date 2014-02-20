import numpy as np
from tmdp.mdp_utils.mdps_utils import all_actions
from tmdp.meat.free_energy.meat import free_energy_iteration
from tmdp.meat.free_energy.report import report_free_energy
from tmdp.solver import SimpleMDPSolver


__all__ = ['FreeEnergySolver']


class FreeEnergySolver(SimpleMDPSolver):

    def __init__(self, beta, max_iterations, use_mdp_guess, z_diff_threshold):
        self.beta = beta
        self.max_iterations = max_iterations
        self.use_mdp_guess = use_mdp_guess
        self.z_diff_threshold = z_diff_threshold

    def solve(self, mdp):
        free_energy_res = free_energy_iteration(mdp,
                                                use_mdp_guess=self.use_mdp_guess,
                              max_iterations=self.max_iterations,
                              beta=self.beta,
                              z_diff_threshold=self.z_diff_threshold)

        policy = free_energy_res['iterations'][-1]['pi']

        res = {}
        res['free_energy_res'] = free_energy_res
        res['policy'] = policy
        return res


    def publish(self, r, mdp, result):  # @UnusedVariable
        report_free_energy(r, mdp, result['free_energy_res'])

        its = result['free_energy_res']['iterations']
        actions = list(all_actions(mdp))
        print 'actions', actions

        f = r.figure()

        with f.plot('pi_hat') as pylab:
            for action in actions:
                x = [it['pi_hat'][action] for it in its]
                pylab.plot(x, '.', label=action)

        with f.plot('median_F') as pylab:
            x = []
            for it in its:
                F = it['F']
                max_for_s = [max(F[s].values()) for s in F]
                median = np.median(max_for_s)
                x.append(median) 
            pylab.plot(x)

        with f.plot('median_Z') as pylab:
            x = []
            for it in its:
                Z = it['Z']
                median = np.median([Z[s] for s in F])
                x.append(median)
            pylab.plot(x)

