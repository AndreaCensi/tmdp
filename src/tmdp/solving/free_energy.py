from collections import defaultdict

import numpy as np
from tmdp.solving.value_iteration_meat import value_diff, get_mdp_policy
import warnings


def free_energy_iteration(mdp, beta, min_iterations=100, max_iterations=100, threshold=1e-8):
    # average state distribution
    p_hat = uniform_state_dist(mdp)
    # average policy
    pi_hat = uniform_actions_dist(mdp)
    # optimal policy, starts as uniform on actions
    pi = dict([(s, uniform_actions_dist(mdp)) for s in mdp.states()])
    # no, use mdp policy
#     pi = get_mdp_policy(mdp, gamma=1)
    # free energy, represented as state -> action -> value,
    # starts at 1.0
    F = {}
    for s in mdp.states():
        F[s] = {}
        for a in mdp.actions():
            F[s][a] = 1.0

    warnings.warn('we do not need this')
#     F = iterate_F(F, mdp, p_hat, pi, pi_hat, beta)
    Z = compute_Z(mdp, pi_hat, F)

    iterations = []
    iterations.append(dict(F=F, p_hat=p_hat, pi_hat=pi_hat, pi=pi, Z=Z))

    for it in range(max_iterations):
        F_2 = iterate_F(F, mdp, p_hat, pi, pi_hat, beta)
        # F_2 = normalize_F(mdp, F_2)
        pi_hat_2 = compute_pi_hat(pi, p_hat)
        Z_2 = compute_Z(mdp, pi_hat, F)
        pi_2 = compute_pi(mdp, pi_hat, Z_2, F)

        F = F_2
        pi = pi_2
        pi_hat = pi_hat_2
        Z = Z_2
        iterations.append(dict(F=F, p_hat=p_hat, pi_hat=pi_hat, pi=pi, Z=Z))

        diff_Z = value_diff(iterations[-1]['Z'],
                            iterations[-2]['Z'])
        Zm = np.mean(Z.values())
        print format_compact(pi_hat)
        print('%5d avg Z: %10.12f   diff_Z : %10.12f' % (it, Zm, diff_Z))
#         if it > min_iterations and diff_Z < threshold:
#             break
    res = {}
    res['params'] = dict(beta=beta, threshold=threshold)
    res['iterations'] = iterations
    return res

def format_compact(p):
    s = ""
    for x, p_x in p.items():
        s += '%s: %.3f ' % (x, p_x)
    return s


#
# def normalize_F(mdp, F):
#     Fsum = 0
#     for s in mdp.states():
#         for a in mdp.actions():
#             Fsum += F[s][a]
#
#     F2 = {}
#     for s in mdp.states():
#         F2[s] = {}
#         for a in mdp.actions():
#             F2[s][a] = F[s][a] / Fsum
#     return F2


def compute_pi(mdp, pi_hat, Z, F):
    pi = {}
    for s in mdp.states():
        pi[s] = {}

        for a in mdp.actions():
            try:
                if F[s][a] < 500:
                    pi[s][a] = pi_hat[a] * np.exp(-F[s][a]) / Z[s]
                else:
                    pi[s][a] = 0
            except FloatingPointError:
                print('pi_hat[a]: %s' % pi_hat[a])
                print('F[s][a]: %s' % F[s][a])
                print('Z[s]: %s' % Z[s])
                raise

        # pi[s] = normalize(pi[s])
    return pi



def normalize(p):
    p_sum = sum(p.values())
    if p_sum == 0:
        r = {}
        for x in p:
            r[x] = 1 / len(p)
        return r
    else:
        r = {}
        for x in p:
            r[x] = p[x] / p_sum
        return r

def compute_Z(mdp, pi_hat, F):
    # Z is a function over states
    Z = {}
    for s in mdp.states():
        Z[s] = 0
        for a, p_a in pi_hat.items():
            try:
                if F[s][a] < 500:
                    Z[s] += p_a * np.exp(-F[s][a])
                else:
                    Z[s] += 0
            except FloatingPointError:
                print('trying to compute exp(%s)' % (-F[s][a]))
                raise
    return Z
    

def compute_pi_hat(pi, p_hat):
    pi_hat = defaultdict(lambda: 0.0)
    for s, p_s in p_hat.items():
        for a, p_s_a in pi[s].items():
            pi_hat[a] += p_s * p_s_a
    return dict(pi_hat)


def iterate_F(F, mdp, p_hat, pi, pi_hat, beta):
    # average over conditional distributions
    F2 = {}
    for s in mdp.states():
        F2[s] = {}
        for a in mdp.actions():
            F2[s][a] = iterate_F_s_a(F, mdp, p_hat, pi, pi_hat, beta, s, a)
    return F2

def iterate_F_s_a(F, mdp, p_hat, pi, pi_hat, beta, s, a):
    # average over dynamics
    p = mdp.transition(s, a)
    res = 0
    for s2, p_s2 in p.items():
        R = mdp.reward(s, a, s2)
        G_ = G(pi, pi_hat, F, s2)
        if p_s2 == 0:
            # print s, a
            # print p
            frac = 0
        else:
            frac = np.log(p_s2) - np.log(p_hat[s2])

        res += p_s2 * (frac - beta * R + G_)
    return res


def G(pi, pi_hat, F, s2):
    # average over actions
    f = 0
    for a2, p_a2 in pi[s2].items():
        if p_a2 == 0:
            frac = 0
        else:
            try:
                frac = np.log(p_a2) - np.log(pi_hat[a2])
            except FloatingPointError:
                print('a2: %s' % a2)
                print('pi_hat[a2]: %s' % pi_hat[a2])
                print('pi_hat: %s' % pi_hat)
                raise
        f += p_a2 * (frac + F[s2][a2])
    return f

def _uniform_dist(what):
    what = list(what)
    n = len(what)
    p = {}
    for s in what:
        p[s] = 1.0 / n
    return p

def uniform_state_dist(mdp):
    """ Returns uniform p.d. over states. """
    return _uniform_dist(mdp.states())

def uniform_actions_dist(mdp):
    """ Returns uniform p.d. over states. """
    return _uniform_dist(mdp.actions())
