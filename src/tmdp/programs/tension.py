

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
