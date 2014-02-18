from collections import defaultdict
from .prob_utils import sample_from_dist

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
    return dict(ds)

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


