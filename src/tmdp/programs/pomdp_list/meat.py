import warnings

from reprep.utils import frozendict2
from tmdp.mdp_utils import all_actions, mdp_stationary_dist
from tmdp.meat.value_it.vit_solver import VITMDPSolver
from tmdp.programs.pomdp_list.agent import create_agent, check_agent

from .disambiguate_imp import disambiguate
from .mdp_builder import MDPBuilder


__all__ = [
   'find_minimal_policy',
   'pomdp_list_states',
]

def find_minimal_policy(res, pomdp):
    """ 
        Assumes res['builder'] is a MDPBuilder
    
        Returns:
        
        res['policy'] = optimal policy
        res2['stationary']
        res['nonneg'] = states tha1t will be seen under the optimal policy
        
        res['mdp_non_absorbing']
        res['mdp_absorbing'] 

        res['trajectories'] 
     """

    print('Start distribution: %s' % pomdp.get_start_dist_dist())
    builder = res['builder']
    print('Creating mdp_absoribing...')
    mdp_absorbing = builder.get_sampled_mdp(goal_absorbing=True)

    
    print('Solving the resulting MDP...')
    solver = VITMDPSolver(least_committed=False)
    res2 = solver.solve(mdp_absorbing)
    policy = res2['policy']
    print('commands used by policy: %s' % list(policy.values()))
#     print('policy: %s' % policy)
 
    # can be big!
    # res2['mdp_absorbing'] = mdp_absorbing
#     res2['mdp_absorbing:desc'] = """
#
#     """

    # Create a nonabsorbing MDP by resetting after getting to the goal.
    print('Creating MDP variation with nonabsorbing states...')
    mdp_non_absorbing = \
        builder.get_sampled_mdp(goal_absorbing=False, stay=0.1)
    # res2['mdp_non_absorbing'] = mdp_non_absorbing

    # Get the stationary distribution of this MDP
    print('Getting the stationary distribution of this MDP...')
    dist0 = mdp_stationary_dist(mdp_non_absorbing,
                                mdp_non_absorbing.get_start_dist(), policy,
                                l1_threshold=1e-8)
    res2['stationary'] = dist0
    res2['stationary:desc'] = """
        Stationary distribution over belief states
    """

    # these are the states that have nonnegligible probability
    nonneg = [s for s in dist0 if dist0[s] >= 1e-4]
    res2['nonneg'] = nonneg
    res2['nonneg:desc'] = """
        Belief states with nonnegligible probability.
    """
    res2['policy:desc'] = """
        Optimal policy: hash belief state -> distribution over actions
    """

    print('Find all trajectories for the POMDP...')
    tjs = get_all_trajectories(pomdp, policy)
#     print('we got %d trajectories.' % len(tjs))
#     for i, t in enumerate(tjs):
#         print(' %d - final %s' % (i, t[-1]))
    # add command "end" in the final step
#     from tmdp.programs.pomdp_list.alternate_observations import add_final
    res2['trajectories'] = tjs
    res2['trajectories:desc'] = """
        These are all possible trajectories in this POMDP. 
        A trajectory is a sequence of dictionaries with fields
            dict(action=action, obs=y,
                belief=belief, belief1=belief1,
                 ydist=ydist, belief2=belief2)
    """
    print('Now I want to see the decisions that we need '
          'to do in the trajectories.')
    res2['decisions'] = set(get_decisions(res2['trajectories']))
    print('Found %d unique decisions' % len(res2['decisions']))
    res2['decisions:desc'] = """
        The decisions that we had to do in the trajectories.
        This is a list of dictionaries.
        Each dict has fields
        "action":
        "state": dict(last=y) 
        "history": list of dictionaries (as above)
    """

    print('Disambiguating states...')
    
    extra_states, decisions_dis = disambiguate(res2['decisions'])
    res2['extra_states'] = extra_states
    res2['extra_states:desc'] = """
        This is a list of dictionary with fields:
            "name":
            "trigger": sequence of observations that should trigger the state
    """
    res2['decisions_dis'] = decisions_dis
    res2['decisions_dis:desc'] = """
     Updated decisions. 
     Now there are potentially new states.
     And there are new actions of the form "state=1)".
    """

    res2['agent'] = create_agent(decisions_dis)
    print('Checking that this agent reconstructs the trajectories exactly'
          ' and adding "agent_state" to the dict.')
    check_agent(res2['agent'], res2['trajectories'])


    print('actions: %s' % list(all_actions(pomdp)))
    print('declare: %s' % pomdp.declare_actions)
    print('...done.')
    return res2



def pomdp_list_states(pomdp, use_fraction=True):
    """ Returns res['builder'] as a MDPBuilder """
    res = {}

    start_dist = pomdp.get_start_dist_dist()
    print('start: %s' % start_dist)

    builder = MDPBuilder(start_dist=start_dist)
    res['builder'] = builder

    nodes_open = list()
    nodes_closed = set()
    nodes_goal = set()

    for belief0, _ in start_dist.items():
        nodes_open.append(belief0)

    actions = all_actions(pomdp)
    while nodes_open:
        if len(nodes_closed) % 100 == 0:
            print('nopen: %5d nclosed: %5d ngoal: %5d'
                  % (len(nodes_open), len(nodes_closed), len(nodes_goal)))
        belief = nodes_open.pop()

        # print('-- popping %s' % belief)
        # assert not belief in nodes_closed

        builder.add_state(belief)

        nodes_closed.add(belief)

        warnings.warn('xxx')
        if pomdp.is_goal_belief(belief):
            nodes_goal.add(belief)
            builder.mark_goal(belief)

#         warnings.warn('Optimization: do not pop goal beliefs')
#         if pomdp.is_goal_belief(belief):
#             continue
#         if pomdp.is_goal_belief(belief):
#             nodes_goal.add(belief)
#             builder.mark_goal(belief)
#         else:
        if True:
            # for each action, evolve belief
            for action in actions:
                belief1 = pomdp.evolve(belief, action,
                                       use_fraction=use_fraction)
                for _, p_x in belief1.items():
                    assert p_x > 0

                # print('-- %s -> %s' % (action, belief1))
                # now sample observations
                ydist = pomdp.get_observations_dist_given_belief(belief1,
                            use_fraction=use_fraction)
                for y, p_y in ydist.items():
                    assert p_y > 0
                    # Now, see what would be the belief for each
                    # possible observation
                    # p(y | x) * p(x) / p(y)
                    # Likelihood

                    # print('y = %s is generated with prob %s ' % (y, p_y))
                    belief2 = pomdp.inference(belief=belief1,
                                              observations=y,
                                              use_fraction=use_fraction)


                    warnings.warn('assuming state2=state')
                    reward = avgreward(pomdp, belief, action)

                    builder.add_transition(belief, action, belief2, p_y, reward)

                    if belief2 in nodes_closed or belief2 in nodes_open:
                        pass
                    else:
                        nodes_open.append(belief2)

    return res

def avgreward(pomdp, belief, action):
    reward = 0
    for state, p_state in belief.items():
        warnings.warn('assuming state2=state')
        state2 = state
        reward += p_state * pomdp.reward(state, action, state2)
    return reward


def get_all_trajectories(pomdp, policy):
    # Get all possible trajectories in an absorbing POMDP.
    # This is done recursively

    trajectories = []
    # For all possible initial belief
    start_dist = pomdp.get_start_dist_dist()
    for belief0, _ in start_dist.items():
        traj = get_all_trajectories_rec(pomdp=pomdp,
                                        policy=policy, belief=belief0)
        trajectories.extend(traj)
    return trajectories


def get_all_trajectories_rec(pomdp, policy, belief, use_fraction=True):
    """ This one first generates an observation. 
    
        for obs in observations:
            for action in actions:
            
    """
    if pomdp.is_goal_belief(belief):
        return [[]]

    belief = frozendict2(belief)
    obs_dist = pomdp.get_observations_dist_given_belief(belief,
                    use_fraction=use_fraction)
    
    trajectories = []

    for obs, _ in obs_dist.items():
        belief_given_obs = pomdp.inference(belief=belief,
                                           observations=obs,
                                           use_fraction=use_fraction)
        assert belief_given_obs in policy
        actions = policy[belief_given_obs].keys()
        for action in actions:
            belief_after_action = pomdp.evolve(belief_given_obs,
                                               action, use_fraction=use_fraction)
            if belief_after_action == belief:
                print('Found fixed point under optimal policy.')
                print(' - belief: %s' % belief)
                print(' - policy: %s' % policy[belief])
                print(' - belief2: %s' % belief)
                raise ValueError()

            rest = get_all_trajectories_rec(pomdp, policy, belief_after_action,
                                            use_fraction=use_fraction)
            for t1 in rest:
                # desc = """
                #     From belief
                #     we sampled obs
                #     then belief1 = belief given obs
                #     then we chose action
                #     then belief2 = belief1 evolved with action.
                # """
                warnings.warn('Need to chenage belief1,2 to meaningful names.')
                traj = [dict(belief=belief, action=action, obs=obs,
                             belief1=belief_given_obs,
                             ydist=obs_dist, belief2=belief_after_action)] + t1
                trajectories.append(traj)

    return trajectories

# @contract(returns='list(list(tuple(*,*)))')
def get_all_trajectories_rec_old(pomdp, policy, belief, use_fraction=True):
    """ This one first asks for an action, then looks for observations. 
    
    
        for action in actions:
            for obs in observations:
    """
    if pomdp.is_goal_belief(belief):
        # return [[]]
        actions = list(policy[belief].keys())
        if len(actions) != 1:
            msg = 'Expected that a goal belief only had 1 action.'
            raise ValueError(msg)
        final_action = actions[0]
        belief1 = belief2 = belief
        ydist = pomdp.get_observations_dist_given_belief(belief1,
                    use_fraction=use_fraction)
        # Just choose first
        final_y = list(ydist)[0]
        traj = [[dict(action=final_action, obs=final_y,
                             belief=belief, belief1=belief1,
                             ydist=ydist, belief2=belief2)]]
        return traj

    belief = frozendict2(belief)
    actions = policy[belief].keys()

    trajectories = []

    for action in actions:
        assert belief in policy

        # evolve the belief given action
        belief1 = pomdp.evolve(belief, action, use_fraction=use_fraction)
        belief1 = frozendict2(belief1)
        # what's the dist of observation given the resulting belief
        ydist = pomdp.get_observations_dist_given_belief(belief1,
                    use_fraction=use_fraction)

        for y, _ in ydist.items():
            belief2 = pomdp.inference(belief=belief1,
                                      observations=y,
                                      use_fraction=use_fraction)

            if belief2 == belief:
                print('Found fixed point under optimal policy.')
                print(' - belief: %s' % belief)
                print(' - policy: %s' % policy[belief])
                print(' - belief2: %s' % belief)
                raise ValueError()
            rest = get_all_trajectories_rec(pomdp, policy, belief2,
                                            use_fraction=use_fraction)
            for t1 in rest:
                traj = [dict(action=action, obs=y,
                             belief=belief, belief1=belief1,
                             ydist=ydist, belief2=belief2)] + t1
                trajectories.append(traj)

    return trajectories

def get_decisions(trajectories):
    """ Returns list of dicts with fields action, state=dict(last=y) 
        and history """
    n = 0
    for tr in trajectories:
        for i in range(len(tr)):
            action = tr[i]['action']
            obs = tr[i]['obs']
            history = tuple([yh['obs'] for yh in tr[:i]])
            n += 1
            # print('%03d: u = %s  y = %s  history %s' % (n, action, obs, len(history)))
            d = dict(action=action,
                    state=frozendict2(last=obs), history=history)
            if 'agent_state' in tr[i]:
                d['agent_state'] = tr[i]['agent_state']
            yield frozendict2(d)
    # print('Found %d raw decisions' % (n))
