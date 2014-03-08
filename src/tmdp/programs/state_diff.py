from contracts import contract

from quickapp import CompmakeContext, QuickApp, iterate_context_names
from reprep import Report
from tmdp import get_conftools_tmdp_smdp_solvers, get_conftools_tmdp_smdps

from .main import TMDP
from .show import instance_mdp
from .solve import jobs_solve
from tmdp.mdp_utils.prob_utils import _uniform_dist
import warnings


__all__ = ['StateDiff']


class StateDiff(TMDP.get_sub(), QuickApp):
    """ Displays some statistics of the solution. """

    cmd = 'state-diff'

    def define_options(self, params):
        params.add_string_list('mdps', help='MDPS')
        params.add_string_list('solvers', help='MDPSolvers')

    @contract(context=CompmakeContext)
    def define_jobs_context(self, context):
        options = self.get_options()

        config_mdps = get_conftools_tmdp_smdps()
        id_mdps = config_mdps.expand_names(options.mdps)

        config_solvers = get_conftools_tmdp_smdp_solvers()
        id_solvers = config_solvers.expand_names(options.solvers)

        for c2, id_mdp in iterate_context_names(context, id_mdps):
            c2.add_extra_report_keys(id_mdp=id_mdp)
            mdp = c2.comp_config(instance_mdp, id_mdp)

            from tmdp.programs.value_iteration import report_mdp_display
            r = c2.comp_config(report_mdp_display, mdp)
            c2.add_report(r, 'report_mdp_display')

            for cc, id_solver in iterate_context_names(c2, id_solvers):
                cc.add_extra_report_keys(id_solver=id_solver)
                solve_result = jobs_solve(cc, mdp, id_solver)
                jobs_analysis(cc, mdp, solve_result)

def jobs_analysis(context, mdp, solve_result):
    r = context.comp(report_diff, mdp, solve_result)
    context.add_report(r, 'report_diff')
    r = context.comp(report_minimization, mdp, solve_result)
    context.add_report(r, 'report_min')

def report_diff(mdp, solve_result):
    policy = solve_result['policy']
    value = solve_result['value']
    tension = get_tension_matrix(mdp, policy, value)
    r = Report()
    f = r.figure()
    print tension
    with f.plot('tension') as pylab:
        mdp.display_neigh_field_value(pylab, tension)
    return r

import numpy as np

def report_minimization(mdp, solve_result):
    policy = solve_result['policy']
    value = solve_result['value']
    warnings.warn('fixing policy')
    for g in mdp.get_goal():
        policy[g] = _uniform_dist(mdp.actions(g))
    tension = get_tension_matrix(mdp, policy, value)

    pos = {}
    for s in mdp.states():
        pos[s] = np.array(s)


    spring_0 = {}
    spring_1 = {}
    Tmax = np.abs(np.array(tension.values())).max()
    for (s1, s2), T in tension.items():
        if s1 == s2:
            print('same state tension: %s' % (s1, s2))
            continue
        Tn = np.abs(T) / Tmax
        # natural distance
        d0 = np.linalg.norm(np.array(s1) - np.array(s2))
        spring_1[(s1, s2)] = Tn
        warnings.warn('temp policy')
        spring_0[(s1, s2)] = d0

    r = Report()

    f = f1
    f_gradient = f1_gradient

    f = f2
    f_gradient = f2_gradient

    plot_result(r, 'start', pos, spring_0)
    
     
    jsteps = 20
    alpha_steps = list(np.linspace(0.0, 1.0, jsteps))
    print alpha_steps
    for j, alpha in enumerate(alpha_steps):
        print j, alpha
        
        spring = average_spring(spring_0, spring_1, alpha)
        pos = gradient_descent(pos=pos, spring=spring,
                               f=f, f_gradient=f_gradient, max_iterations=400,
                               mean_dist_threshold=0.01, alpha=0.1)

        print('plot %s.. ' % str((j, alpha)))
        plot_result(r, j, pos, spring_1)
        print('...done')

    return r

def gradient_descent(pos, spring, f, f_gradient, max_iterations, mean_dist_threshold, alpha):
    # threshold:
    for i in range(1, max_iterations):
        obj = f(spring, pos)
#         print('iteration %3d: value: %10.4f' % (i, obj))
        g1 = f_gradient(spring, pos)
        pos1 = {}
        for s in pos:
            pos1[s] = pos[s] - alpha * g1[s]

        sum_dist = 0
        for s in pos:
            sum_dist += np.abs(pos1[s] - pos[s])
        mean_dist = np.mean(sum_dist)

        print('iteration %3d: value: %10.4f mean_change: %10.5f' % (i, obj, mean_dist))
        pos = pos1

        if mean_dist < mean_dist_threshold:
            break
    return pos

def average_spring(spring0, spring1, alpha):
    res = {}
    for s in spring0:
        res[s] = spring0[s] * (1 - alpha) + alpha * spring1[s]
    return res
# L2
def f2(spring, pos):
    res = 0.0
    for (s1, s2), T in spring.items():
        res += (np.linalg.norm(pos[s1] - pos[s2]) - T) ** 2
    return res

def f2_gradient(spring, pos):
    res = {}
    for s in pos:
        res[s] = f2_gradient_s(spring, pos, s)
    
    return res
    
def f2_gradient_s(spring, pos, s):
    """ Gradient with respect to s """
    res = np.array([0.0, 0.0])
    for (s1, s2), T in spring.items():
        if s1 != s:
            continue
        p1 = pos[s1]
        p2 = pos[s2]
        grad = (np.linalg.norm(p1 - p2) - T) * (p1 - p2)
        res += grad
    return res
    
# L1
def f1(spring, pos):
    res = 0.0
    for (s1, s2), T in spring.items():
        res += np.abs(np.linalg.norm(pos[s1] - pos[s2]) - T)
    return res

def f1_gradient(spring, pos):
    res = {}
    for s in pos:
        res[s] = f1_gradient_s(spring, pos, s)

    return res

def f1_gradient_s(spring, pos, s):
    """ Gradient with respect to s """
    res = np.array([0.0, 0.0])
    for (s1, s2), T in spring.items():
        if s1 != s:
            continue
        p1 = pos[s1]
        p2 = pos[s2]
        grad = np.abs(np.linalg.norm(p1 - p2) - T) * (p1 - p2)
        res += grad
    return res

def plot_result(r, i, pos, tension):
    values = np.abs(np.array(tension.values()))
    f = r.figure('it%s' % i)
    with f.plot('pos') as pylab:
        for s, y in pos.items():
            pylab.plot(y[0], y[1], '.')
        for (s1, s2), T in tension.items():
            Tn = np.abs(T) / values.max()
            y1 = pos[s1]
            y2 = pos[s2]
            pylab.plot((y1[0], y2[0]), [y1[1], y2[1]], '-',
                       color=[1 - Tn, 1 - Tn, 1 - Tn])


def get_tension_matrix(mdp, policy, value):
    # Returns dict ( (state, state) -> real )
    T = {}
    for s1 in mdp.states():
        for s2 in mdp_state_neighbors(mdp, s1):
            T[(s1, s2)] = mdp_state_tension(mdp, s1, s2, policy, value)
            T[(s2, s1)] = T[(s1, s2)]  # for absorbing states...

    for s1 in mdp.states():
        for s2 in mdp_state_neighbors(mdp, s1):
            assert (s1, s2) in T
            if not (s2, s1) in T:
                msg = 'Could find %s but not %s' % ((s1, s2), (s2, s1))
                assert (s2, s1) in T, msg
    return T

def mdp_state_neighbors(mdp, s):
    """ Returns the states that are considered neighbors. """
    neigh = set()
    for a in mdp.actions(s):
        for s2 in mdp.transition(s, a):
            if not s == s2:
                neigh.add(s2)
    return neigh

def mdp_state_tension(mdp, s1, s2, policy, value):
    a1 = mdp.actions(s1)
    a2 = mdp.actions(s2)
    if not set(a1) == set(a2):
        msg = 'States dont have same actions.'
        raise ValueError(msg)
    # simple way: what happens if the policy of one is used in the other
    R1 = mdp_value_given_policy_in_s(mdp, s1, policy[s1], value)
    R2 = mdp_value_given_policy_in_s(mdp, s2, policy[s2], value)
    R1b = mdp_value_given_policy_in_s(mdp, s1, policy[s2], value)
    R2b = mdp_value_given_policy_in_s(mdp, s2, policy[s1], value)
    tension = 0.5 * ((R1b + R2b) - (R1 + R2))
    assert tension <= 0
    return tension


    
def mdp_reward_given_action_in_s(mdp, s, a):
    return sum([p_s2 * mdp.reward(s, a, s2) for s2, p_s2 in mdp.transition(s, a).items()])

def mdp_reward_given_policy_in_s(mdp, s, a_dist):
    R = sum([p_a * mdp_reward_given_action_in_s(mdp, s, a) for a, p_a in a_dist.items()])
    return R
     

def mdp_value_given_action_in_s(mdp, s, a, V):
    return sum([p_s2 * V[s2] for s2, p_s2 in mdp.transition(s, a).items()])

def mdp_value_given_policy_in_s(mdp, s, a_dist, V):
    R = sum([p_a * mdp_value_given_action_in_s(mdp, s, a, V) for a, p_a in a_dist.items()])
    return R

