import numpy as np

def get_mdp_policy(mdp, gamma):
    """ Returns  policy """
    values = vit_solve(mdp, gamma=gamma, threshold=1e-7)
    policy = policy_from_value(mdp, values, gamma=gamma)
    return policy

def policy_from_value(mdp, values, gamma=1.0):
    """ values: state -> value """
    P = {}
    for s in mdp.states():
        P[s] = { best_action(mdp, values, s): 1.0 }
    return P

def best_action(mdp, V, s, gamma=1):
    actions = list(mdp.actions())
    vs = [Q(mdp, V, s, a, gamma=gamma)
          for a in actions]
    best = np.argmax(vs)
    return actions[best]

def Q(mdp, V, s, a, gamma=1):
    f_a = 0
    p_s_a = mdp.transition(s, a)
    for s2, p_s2 in p_s_a.items():
        R_s_s2_a = mdp.reward(s, a, s2)
        f_a += p_s2 * (R_s_s2_a + gamma * V[s2])
    return f_a

def vit_solve(mdp, gamma=1, threshold=1e-7):
    V = {}
    for s in mdp.states():
        V[s] = 0

    while True:
        V2 = {}
        for s in mdp.states():
            vs = [Q(mdp, V, s, a, gamma=gamma)
                  for a in mdp.actions()]
            V2[s] = max(vs)
        change = value_diff(V, V2)
        # print('Change: %s' % change)
        V = V2
        if change < threshold:
            break

    return V

def value_diff(V1, V2):
    res = 0
    for s in V1:
        res += np.abs(V1[s] - V2[s])
    return res



