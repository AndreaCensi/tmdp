from tmdp.mdp_utils import all_actions, mdp_stationary_dist
from tmdp.meat.value_it.vit_solver import VITMDPSolver

from .disambiguate_imp import disambiguate
from .mdp_builder import MDPBuilder
from .report_aliasing_imp import get_all_trajectories, \
    get_decisions


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
        res['nonneg'] = states that will be seen under the optimal policy
        
        res['mdp_non_absorbing']
        res['mdp_absorbing'] 

        res['trajectories'] 
     """

    builder = res['builder']
    print('Creating mdp_absoribing...')
    mdp_absorbing = builder.get_sampled_mdp(goal_absorbing=True)

    print('Solving the resulting MDP...')
    solver = VITMDPSolver(least_committed=False)
    res2 = solver.solve(mdp_absorbing)
    policy = res2['policy']

    # Create a nonabsorbing MDP by resetting after getting to the goal.
    print('Creating MDP variation with nonabsorbing states...')
    mdp_non_absorbing = builder.get_sampled_mdp(goal_absorbing=False, stay=0.1)

    # Get the stationary distribution of this MDP
    print('Getting the stationary distribution of this MDP...')
    dist0 = mdp_stationary_dist(mdp_non_absorbing,
                                mdp_non_absorbing.get_start_dist(), policy,
                                l1_threshold=1e-8)

    # these are the states that have nonnegligible probability
    nonneg = [s for s in dist0 if dist0[s] >= 1e-4]

    res2['mdp_non_absorbing'] = mdp_non_absorbing
    res2['mdp_absorbing'] = mdp_absorbing
    res2['stationary'] = dist0
    res2['nonneg'] = nonneg
    res2['policy'] = policy
    res2['policy:desc'] = """
        Optimal policy: hash belief state -> distribution over actions
    """

    print('Find all trajectories for the POMDP...')
    res2['trajectories'] = get_all_trajectories(pomdp, policy)
    res2['trajectories:desc'] = """
        These are all possible trajectories in this POMDP. 
        A trajectory is a sequence of tuples (observations, action).
    """
    print('Now I want to see the decisions that we need to do in the trajectories.')
    res2['decisions'] = set(get_decisions(res2['trajectories']))
    res2['decisions:desc'] = """
        The decisions that we had to do in the trajectories.
        This is a list of dictionaries.
        Each dict has fields
        "action":
        "state": dict(last=y) 
        "history": list of tuples (observation, action) leading here.
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
            print('nopen: %5d nclosed: %5d ngoal: %5d' % (len(nodes_open), len(nodes_closed), len(nodes_goal)))
        belief = nodes_open.pop()

        # print('-- popping %s' % belief)
        # assert not belief in nodes_closed

        builder.add_state(belief)

        nodes_closed.add(belief)

        if pomdp.is_goal_belief(belief):
            nodes_goal.add(belief)
            builder.mark_goal(belief)

#             for action in actions:
#                 for belief0, p0 in start_dist.items():
#                     builder.add_transition(belief, action, belief0, p0, 0)

            # any action at the goal states makes it go randomly to the initial states
#             for action in actions:
#                 for belief0, p0 in start_dist.items():
#                     builder.add_transition(belief, action, belief0, p0, 0)

            # print('goal: %s' % belief)
        else:
            # for each action, evolve belief
            for action in actions:
                belief1 = pomdp.evolve(belief, action, use_fraction=use_fraction)
                for _, p_x in belief1.items():
                    assert p_x > 0

                # print('-- %s -> %s' % (action, belief1))
                # now sample observations
                for y, p_y in pomdp.get_observations_dist_given_belief(belief1, use_fraction=use_fraction).items():
                    assert p_y > 0
                        # Now, see what would be the belief for each possible observation
                    # p(y | x) * p(x) / p(y)
                    # Likelihood

                    # print('y = %s is generated with prob %s ' % (y, p_y))
                    belief2 = pomdp.inference(belief=belief1, observations=y, use_fraction=use_fraction)

                    builder.add_transition(belief, action, belief2, p_y, -1)

                    if belief2 in nodes_closed or belief2 in nodes_open:
                        pass
                    else:
                        nodes_open.append(belief2)

#             if np.random.rand() < 0.01:
#                 print('last opened: %s' % belief)

    return res
