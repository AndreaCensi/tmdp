from collections import defaultdict

from contracts import contract
from numpy.testing.utils import assert_allclose

from ddist import ddist_diff_l1, ddist_evolve
import ddist  # @UnusedImport
from tmdp.mdp import SimpleMDP

from .prob_utils import sample_from_dist


def is_uniform(mdp):
    """ Returns true if all actions are available in all states. """
    all_a = set(all_actions(mdp))
    for s in mdp.states():
        if not set(mdp.actions(s)) == all_a:
            return False
    return True

def all_actions(mdp):
    print('looking at all actions')
    actions = set()
    for s in mdp.states():
        actions.update(mdp.actions(s))
    print('done')
    return sorted(list(actions))


def run_trajectories(mdp, start, policy, nsteps, ntraj, goal):
    """ Returns prob. dist over states. """
    ds = defaultdict(lambda:0)
    for _ in range(ntraj):
        s0 = sample_from_dist(start)
        states = run_trajectory(mdp, s0, policy, nsteps, goal)
        if not states[-1] in goal:
            continue
        for s in states:
            ds[s] += (1.0 / ntraj) * (1.0 / len(states))
    return dict(ds)  # XXX


@contract(mdp=SimpleMDP, dist0='ddist', returns='ddist')
def mdp_evolve_with_policy(mdp, dist0, policy):
    """ Evolves the distribution under the given policy. """
    res = defaultdict(lambda: 0.0)
    for s, p_s in dist0.items():
        for a, p_a in policy[s].items():
            for s2, p_s2 in mdp.transition(s, a).items():
                p = p_s * p_a * p_s2
                if p > 0:
                    res[s2] += p
    return dict(**res)


def ddist_format_states(states, dist):
    res = ''
    for s in states:
        if s in dist:
            p = dist[s]
            res += ('%8.2f ' % float(p))
        else:
            res += '%8.0f' % 0
    return res


@contract(mdp=SimpleMDP, dist0='ddist')
def mdp_stationary_dist(mdp, dist0, policy, l1_threshold=0.0):
    """ Find the stationary distribution. """

    T = mdp_get_transition_with_policy(mdp, policy)
    # print('transition: %s' % T)

    dist = dict(**dist0)

    # print('dist0: %s' % ddist_format_states(mdp.states(), dist))
    while True:
        dist2 = ddist_evolve(dist, T)
        diff = ddist_diff_l1(dist, dist2)
        # print('dist cur: %s' % ddist_format_states(mdp.states(), dist2))
        # print('difference: %10.8f' % diff)
        dist = dist2

        if diff <= l1_threshold:
            break
    return dist

@contract(mdp=SimpleMDP, returns='cond_ddist')
def mdp_get_transition_with_policy(mdp, policy):
    """ Gets the transition resulting from using the policy. """
    res = {}
    for s in mdp.states():
        given_s = defaultdict(lambda: 0.0)
        for a, p_a in policy[s].items():
            for s2, p_s2 in mdp.transition(s, a).items():
                p = p_a * p_s2
                if p > 0:
                    given_s[s2] += p
        res[s] = dict(**given_s)
    return res
    

def run_trajectory(mdp, start, policy, nsteps, goal):
    state = start
    traj = []
    for _ in range(nsteps):
        traj.append(state)
        if state in goal:
            break
        action = sample_from_dist(policy[state])
        state2_dist = mdp.transition(state, action)
        state = sample_from_dist(state2_dist)
    return traj


def assert_is_dist(p):
    assert isinstance(p, dict)
    assert_allclose(sum(p.values()), 1.0)


def assert_is_conditional(p):
    assert isinstance(p, dict)
    for q in p.values():
        assert_is_dist(q)


def dist_evolve(p, conditional):
    """ p: state -> prob
        conditional: state -> state """
    assert_is_dist(p)
    assert_is_conditional(conditional)

    res = defaultdict(lambda:0.0)
    for s, p_s in p.items():
        for s2, p_s2 in conditional[s].items():
            res[s2] += p_s * p_s2

    res = dict(**res)
    assert_is_dist(res)
    return res







    
