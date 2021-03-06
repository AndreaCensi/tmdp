from collections import defaultdict
import warnings

import numpy as np
from tmdp.mdp_utils import all_actions
from tmdp.mdp_utils.prob_utils import _uniform_dist, _random_dist
from tmdp.meat.value_it.meat import value_diff, get_mdp_policy


def free_energy_iteration(mdp, beta, use_mdp_guess, max_iterations,
                          z_diff_threshold, min_iterations=4):
    # average state distribution
    p_hat = uniform_state_dist(mdp)
    # average policy
    pi_hat = uniform_actions_dist(mdp)
    # optimal policy, starts as uniform on actions

    if use_mdp_guess:
        print('Using MDP guess')
        pi = get_mdp_policy(mdp, gamma=1)
    else:
        print('Using random guess')

        # pi = dict([(s, _uniform_dist(mdp.actions(s))) for s in mdp.states()])
        pi = dict([(s, _random_dist(mdp.actions(s))) for s in mdp.states()])

    # free energy, represented as state -> action -> value,
    F = {}
    for s in mdp.states():
        F[s] = {}
        for a in mdp.actions(s):
            warnings.warn('using random free energy')
            F[s][a] = 0.0
            F[s][a] = np.random.rand()

    Z = compute_Z(mdp, pi_hat, F)

    iterations = []
    iterations.append(dict(F=F, p_hat=p_hat, pi_hat=pi_hat, pi=pi, Z=Z))

    for it in range(max_iterations):
        F_2 = iterate_F(F=F, mdp=mdp, p_hat=p_hat, pi=pi, pi_hat=pi_hat, beta=beta)
        pi_hat_2 = compute_pi_hat(pi, p_hat)
        Z_2 = compute_Z(mdp, pi_hat, F_2)
        pi_2 = compute_pi(mdp, pi_hat, Z_2, F_2)

        F = F_2
        pi = pi_2
        pi_hat = pi_hat_2
        Z = Z_2
        iterations.append(dict(F=F, p_hat=p_hat, pi_hat=pi_hat, pi=pi, Z=Z))

        diff_F = get_diff_F(iterations[-2]['F'], iterations[-1]['F'])
        diff_Z = value_diff(iterations[-1]['Z'], iterations[-2]['Z'])
        Zm = np.mean(Z.values())
        # print format_compact(pi_hat)
        print('%5d avg Z: %10.12f  diff_F: %20.8f diff_Z : %10.12f' % (it, Zm, diff_F, diff_Z))
        if it > min_iterations and diff_F < z_diff_threshold:
            break
    res = {}
    res['params'] = dict(beta=beta, z_diff_threshold=z_diff_threshold,
                         max_iterations=max_iterations, use_mdp_guess=use_mdp_guess,
                         min_iterations=min_iterations)
    res['iterations'] = iterations
    return res

def get_diff_F(F1, F2):
    d = 0
    for s in F1:
        for a in F1[s]:
            d += np.abs(F1[s][a] - F2[s][a])
    return d

# 
# def format_compact(p):
#     s = ""
#     for x, p_x in p.items():
#         s += '%s: %.3f ' % (x, p_x)
#     return s


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

        for a in mdp.actions(s):
            try:
                if F[s][a] < 500:
                    pi[s][a] = pi_hat[a] * np.exp(-F[s][a]) / Z[s]
                else:
                    print('approximating because F = %s' % F[s][a])
                    pi[s][a] = 0.0
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
        Z[s] = 0.0
        s_actions = mdp.actions(s)
        for a, p_a in pi_hat.items():
            if not a in s_actions:
                continue
            try:
                if F[s][a] < 500:
                    Z[s] += p_a * np.exp(-F[s][a])
                else:
                    print('approximating because F = %s' % F[s][a])
                    Z[s] += 0.0
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
        for a in mdp.actions(s):
            if s in mdp.get_goal():
#                 warnings.warn('boundary condition strange')
                F2[s][a] = 0.0
#                 F2[s][a] = 100.0
            else:
                F2[s][a] = iterate_F_s_a(F=F, mdp=mdp, p_hat=p_hat, pi=pi,
                                         pi_hat=pi_hat, beta=beta, s=s, a=a)
    return F2


def iterate_F_s_a(F, mdp, p_hat, pi, pi_hat, beta, s, a):
    assert a in mdp.actions(s)
    # average over dynamics

    res = 0.0
    for s2, p_s2 in mdp.transition(s, a).items():
        R = mdp.reward(s, a, s2)
        G_ = G(mdp, pi, pi_hat, F, s2)
        if p_s2 == 0:
            frac = 0.0
        else:
            frac = np.log(p_s2) - np.log(p_hat[s2])

        res += p_s2 * (frac - beta * R + G_)
    return res


def G(mdp, pi, pi_hat, F, s2):
    # average over actions
    f = 0.0
    for a2, p_a2 in pi[s2].items():
        assert a2 in mdp.actions(s2)
        if p_a2 == 0:
            print a2, p_a2
            frac = 0.0
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


def uniform_state_dist(mdp):
    """ Returns uniform p.d. over states. """
    return _uniform_dist(mdp.states())


def uniform_actions_dist(mdp):
    """ Returns uniform p.d. over states. """
    return _uniform_dist(all_actions(mdp))


