from collections import defaultdict

from .prob_utils import sample_from_dist
from numpy.testing.utils import assert_allclose


def all_actions(mdp):
    actions = set()
    for s in mdp.states():
        actions.update(mdp.actions(s))
    return sorted(list(actions))


def run_trajectories(mdp, start, policy, nsteps, ntraj, stop_at):
    """ Returns prob. dist over states. """
    ds = defaultdict(lambda:0)
    for _ in range(ntraj):
        states = run_trajectory(mdp, start, policy, nsteps, stop_at)
        if states[-1] != stop_at:
            continue
        for s in states:
            ds[s] += (1.0 / ntraj) * (1.0 / len(states))
    return dict(ds)  # XXX


def run_trajectory(mdp, start, policy, nsteps, stop_at):
    state = start
    traj = []
    for _ in range(nsteps):
        traj.append(state)
        if state == stop_at:
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
    print p
    print conditional
    print res
    assert_is_dist(res)
    return res
    
