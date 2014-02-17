from itertools import product

from contracts import contract

from tmdp import SimpleMDP


@contract(m=SimpleMDP)
def checks_mdp(m):

    for s in m.states():
        m.is_state(s)

    for a in m.actions():
        m.is_action(a)

    for (s,a) in product(m.states(), m.actions()):
        r = m.reward(s, a)
        assert r >= 0
        p_s_a = m.transition(s, a)
        m.is_state_dist(p_s_a)

    actions = list(m.actions())
    states = list(m.states())
    p0 = {states[0]: 1.0}
    m.is_state_dist(p0)
    p1 = m.evolve(p0, actions[0])
    print p1
    m.is_state_dist(p1)
