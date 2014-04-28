from reprep import Report
from contracts import contract
from reprep.utils.frozen import frozendict2
from tmdp.programs.pomdp_list.disambiguate_imp import disambiguate


__all__ = ['report_aliasing']


def get_all_trajectories(pomdp, policy):
    # Get all possible trajectories in an absorbing POMDP.
    # This is done recursively

    trajectories = []
    # For all possible initial belief
    start_dist = pomdp.get_start_dist_dist()
    for belief0, _ in start_dist.items():
        traj = get_all_trajectories_rec(pomdp=pomdp, policy=policy, belief=belief0)
        trajectories.extend(traj)
    return trajectories


# @contract(returns='list(list(tuple(*,*)))')
def get_all_trajectories_rec(pomdp, policy, belief, use_fraction=True):
    if pomdp.is_goal_belief(belief):
        return [[]]

    belief = frozendict2(belief)
    actions = policy[belief].keys()

    trajectories = []

    for action in actions:
        assert belief in policy

        # evolve the belief given action
        belief1 = pomdp.evolve(belief, action, use_fraction=use_fraction)
        belief1 = frozendict2(belief1)
        # what's the dist of observation given the resulting belief
        ydist = pomdp.get_observations_dist_given_belief(belief1, use_fraction=use_fraction)
    
        for y, _ in ydist.items():
            belief2 = pomdp.inference(belief=belief1, observations=y, use_fraction=use_fraction)
            rest = get_all_trajectories_rec(pomdp, policy, belief2, use_fraction=use_fraction)
            for t1 in rest:
                traj = [(action, y)] + t1
                trajectories.append(traj)
        
    return trajectories 

def get_decisions(trajectories):
    """ Returns list of dicts with fields action, state=dict(last=y) and history """
    for tr in trajectories:
        for i in range(len(tr)):
            action, y = tr[i]
            history = tuple([yh for (_, yh) in tr[:i]])
            yield frozendict2(action=action, state=frozendict2(last=y), history=history)



def report_aliasing(res, pomdp):
    mdp = res['mdp_absorbing']
    nonneg = res['nonneg']
    stationary = res['stationary']
    policy = res['policy']

    trajectories = get_all_trajectories(pomdp, policy)
    print(' I obtained %d trajectories' % len(trajectories))
    for tr in trajectories:
        print('- %s' % tr)
    



    r = Report()

    print 'start'
    print mdp.get_start_dist()
    print 'goals'
    print mdp.get_goals()

    rows = []
    states_list = []
    for s in nonneg:
        rows.append(pretty_info_state(s))
        p_stationary = stationary[s]
        is_goal = mdp.is_goal(s)
        states_list.append([p_stationary, is_goal])

    cols = ['p_stat', 'is_goal']
#
#     r.table('states', data=states_list, rows=rows, cols=cols,
#                       caption='table of states')


    print('Now I want to see the decisions')
    decisions = set(get_decisions(trajectories))
    
    with r.subsection('decisions1') as sub:
        add_table_decisions(sub, decisions)

    decisions2 = disambiguate(decisions)


    with r.subsection('decisions2') as sub:
        add_table_decisions(sub, decisions2)

    return r

def add_table_decisions(r, decisions):
    data = []
    for d  in decisions:
        action = d['action']
        history = d['history']
        state = d['state']
        data.append([str(action), str(state), str(history[::-1])])
    r.table('decisions', data=data, rows=[''] * len(data),
            cols=['action', 'y', 'history'])



def pretty_info_state(istate):
    s = []
    for state, p_state in istate.items():
        s.append('%s:%s' % (pretty_state(state), pretty_prob(p_state)))
    return '{' + ",".join(s) + "}"


def pretty_state(istate):
    robot, intruder = istate
    return '%s|%s' % (robot, intruder)


def pretty_prob(p_state):
    n = p_state.numerator
    d = p_state.denominator
    return '%s/%s' % (n, d)

