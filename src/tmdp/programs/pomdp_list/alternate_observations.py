from tmdp.programs.pomdp_list.agent import check_agent, create_agent, Namer
from tmdp.programs.pomdp_list.disambiguate_imp import disambiguate
from tmdp.programs.pomdp_list.meat import get_decisions


def create_alternate_trajectories(trajectories, pomdp, pomdp2, rename_obs=True):
#     res2['trajectories'] = get_all_trajectories(pomdp, policy)
#     res2['trajectories:desc'] = """
#         These are all possible trajectories in this POMDP.
#         A trajectory is a sequence of dictionaries with fields
#             dict(action=action, obs=y,
#                 belief=belief, belief1=belief1,
#                  ydist=ydist, belief2=belief2)

#     def get_zdist(belief):
#         zdist = defaultdict(lambda: Fraction(0))
#         for state, p_state in belief.items():
#             for z, p_z in state2zdist(pomdp, state=state, horizon=horizon).items():
#                 zdist[z] += p_state * p_z
#         return frozendict2(zdist)
    namer = Namer('z%d')

    trajectories2 = []
    for traj in trajectories:

        get_belief_for_trajectory(pomdp, traj)
#         print('---')
        traj2 = []
        for x in traj:
            belief = x['belief2']
            belief_back = x['belief_back']
            # TODO: check consistency
#             print('belief: %s\nbelief_back: %s' % (belief, belief_back))
            zdist = pomdp2.get_observations_dist_given_belief(belief_back)
            if len(zdist) != 1:
                msg = ('We cannot sample from this distribution uniquely.'
                       '\np(x): %s\np(z):%s' % (belief, zdist))
                raise ValueError(msg)
            z = list(zdist.keys())[0]
            # y = x['obs']

#             warnings.warn('This is specific to debug intruder POMDP')
#             if y[1] != z[1]:
#                 msg = 'belief2:      %s' % (belief)
#                 msg += '\nbelief_back:  %s' % (belief_back)
#                 msg += '\ny: %s' % str(y)
#                 msg += '\nz: %s' % str(z)
#                 raise ValueError(msg)

            if rename_obs:
                # oz = z
                z = namer(z)
#                 print('%s = %s' % (z, oz))

            action = x['action']
            belief2 = x['belief2']  # not sure here about belief vs belief2
            x2 = dict(action=action, belief=belief, belief2=belief2, obs=z)
            traj2.append(x2)
        assert len(traj2) == len(traj)

        trajectories2.append(traj2)

    assert len(trajectories2) == len(trajectories)

    return trajectories2


def get_belief_for_trajectory(pomdp, trajectory):
    # we know the final belief
    belief_end = trajectory[-1]['belief2']
    if len(belief_end) != 1:
        msg ='I assume that at the end everything is known: %s' % belief_end
        raise ValueError(msg)
        
    trajectory[-1]['belief_back'] = pomdp.evolve_back(belief_end, trajectory[-1]['action'])


    for k in range(len(trajectory) - 1)[::-1]:
        action = trajectory[k]['action']
        belief_back = trajectory[k + 1]['belief_back']
        b0 = pomdp.evolve_back(belief_back, action)
        trajectory[k]['belief_back'] = b0
#         print('-----')
#         print('belief: %s' % str(trajectory[k]['belief']))
#         print('belief2: %s' % str(trajectory[k]['belief2']))
#         print('belief_back: %s' % b0)
#         warnings.warn('specific, get rid')

        

#
# def add_final(trajectories):
#     tjs = []
#     for t in trajectories:
#         x = t[-1]
#         y = dict(belief=x['belief'], belief2=x['belief2'], action='end', obs=x['obs'])
#         tjs.append(list(t) + [y])
#     return tjs

def alternate_observersations_an(res, pomdp, pomdp2, rename_obs):
    # trajectories = add_final(res['trajectories'])
    trajectories = res['trajectories']
#     print('We have %d trajectories' % len(trajectories))
#     for i, t in enumerate(trajectories):
#         print(i, t[-1])

    trajectories2 = create_alternate_trajectories(trajectories, pomdp=pomdp, pomdp2=pomdp2,
                                                  rename_obs=rename_obs)
#     print('become')
#     for i, t in enumerate(trajectories2):
#         print(i, t[-1])

    if not check_realizable(trajectories2):
        raise ValueError('Not realizable')

    decisions2 = set(get_decisions(trajectories2))
    extra_states, decisions2_dis = disambiguate(decisions2)  # @UnusedVariable

    agent2 = create_agent(decisions2_dis)
    print('Checking that this agent reconstructs the trajectories exactly'
          ' and adding "agent_state" to the dict.')
    check_agent(agent2, trajectories2)

    return dict(agent=agent2, trajectories=trajectories2)


def check_realizable(trajectories):
    decisions = get_decisions(trajectories)
    context2action = {}
    for d in decisions:
        action = d['action']
        state = d['state']
        history = d['history']
        context = (history, state)
        if context in context2action:
            action0 = context2action[context]
            if action != action0:
                msg = 'Action conflict:\naction0 %s\naction %s\nstate %s\nhistory %s' % (action0, action, state, history)
                print msg
                return False
        else:
            context2action[context] = action
#             print context
#             print action
            print action, state  # , history
    return True
