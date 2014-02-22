import numpy as np
from tmdp.meat.value_it.meat import value_diff
from tmdp.mdp_utils.prob_utils import _random_dist


__all__ = ['inforl']

def inforl(mdp, beta, use_mdp_guess, max_iterations,
                          z_diff_threshold, min_iterations=4):
    # policy prior
    rho = dict([(s, _random_dist(mdp.actions(s))) for s in mdp.states()])

    # Initialize F to zero.
    F = {}
    for s in mdp.states():
        F[s] = 0.0

    Z = compute_Z(mdp=mdp, beta=beta, rho=rho, F=F)

    iterations = []
    iterations.append(dict(F=F, Z=Z, pi=rho))

    for it in range(max_iterations):
        Z_2 = compute_Z(mdp=mdp, beta=beta, rho=rho, F=F)
        F_2 = compute_F_from_Z(Z=Z_2)

        pi = compute_policy(mdp=mdp, beta=beta, rho=rho, F=F, Z=Z)
        F = F_2
        Z = Z_2
        iterations.append(dict(F=F, Z=Z, pi=pi))

        diff_F = value_diff(iterations[-2]['F'], iterations[-1]['F'])
        diff_Z = value_diff(iterations[-2]['Z'], iterations[-1]['Z'])
        # print format_compact(pi_hat)
        print('%5d  diff_F: %20.8f diff_Z : %10.12f' % (it, diff_F, diff_Z))
        if it > min_iterations and diff_F < z_diff_threshold:
            break

    res = {}
    res['params'] = dict(beta=beta, z_diff_threshold=z_diff_threshold,
                         max_iterations=max_iterations, use_mdp_guess=use_mdp_guess,
                         min_iterations=min_iterations)
    res['iterations'] = iterations
    return res

def compute_policy(mdp, beta, rho, F, Z):
    """ Computes the policy pi_star. """
    pi = {}
    for s in mdp.states():
        pi[s] = {}
        for a in mdp.actions(s):
            x = 0.0
            for s2, p_s2 in mdp.transition(s, a).items():
                x += p_s2 * (beta * mdp.reward(s, a, s2) - F[s2])
            pi[s][a] = (rho[s][a] / Z[s]) * np.exp(x)
    return pi

def compute_Z(mdp, beta, rho, F):
    Z = {}
    for s in mdp.states():
        # average over actions given by the rho policy
        Z[s] = 0.0
        for a, rho_a in rho[s].items():
            x = 0.0
            for s2, p_s2 in mdp.transition(s, a).items():
                x += p_s2 * (beta * mdp.reward(s, a, s2) - F[s2])
            Z[s] += rho_a * np.exp(x)
    return Z

def compute_F_from_Z(Z):
    F = {}
    for s in Z:
        F[s] = -np.log(Z[s])
    return F

def get_diff_F(F1, F2):
    d = 0
    for s in F1:
        for a in F1[s]:
            d += np.abs(F1[s][a] - F2[s][a])
    return d

