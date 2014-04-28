from tmdp.mdp_utils import all_actions, mdp_stationary_dist
from tmdp.meat.value_it.vit_solver import VITMDPSolver
from tmdp.programs.pomdp_list.mdp_builder import MDPBuilder


__all__ = ['find_minimal_policy', 'pomdp_list_states']

def find_minimal_policy(res):
    """ 
        Assumes res['builder'] is a MDPBuilder
    
        Returns:
        
        res['policy'] = optimal policy
        res2['stationary']
        res['nonneg'] = states that will be seen under the optimal policy
        
        res['mdp_non_absorbing']
        res['mdp_absorbing'] 

     """

    builder = res['builder']
    mdp_absorbing = builder.get_sampled_mdp(goal_absorbing=True)
    solver = VITMDPSolver(least_committed=False)

    res2 = solver.solve(mdp_absorbing)
    policy = res2['policy']

    # Create a nonabsorbing MDP by resetting after getting to the goal.
    mdp_non_absorbing = builder.get_sampled_mdp(goal_absorbing=False, stay=0.1)

    # Get the stationary distribution of this MDP
    dist0 = mdp_stationary_dist(mdp_non_absorbing,
                                mdp_non_absorbing.get_start_dist(), policy,
                                l1_threshold=1e-8)

    # these are the states that have nonnegligible probability
    nonneg = [s  for s in dist0 if dist0[s] >= 1e-4]

    res2['mdp_non_absorbing'] = mdp_non_absorbing
    res2['mdp_absorbing'] = mdp_absorbing
    res2['stationary'] = dist0
    res2['nonneg'] = nonneg
    res2['policy'] = policy

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
