from reprep import Report


__all__ = ['report_aliasing']


def report_aliasing(res, pomdp):
    mdp = res['mdp_absorbing']
    nonneg = res['nonneg']
    stationary = res['stationary']

    r = Report()
    rows = []
    states_list = []
    for s in nonneg:
        rows.append(pretty_info_state(s))
        p_stationary = stationary[s]
        is_goal = mdp.is_goal(s)
        states_list.append([p_stationary, is_goal])


    decisions = res['decisions']
    with r.subsection('decisions1') as sub:
        add_table_decisions(sub, decisions)

    decisions2 = res['decisions_dis']

    with r.subsection('decisions_dis') as sub:
        add_table_decisions_only_states(sub, decisions2)

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

def add_table_decisions_only_states(r, decisions):
    states = set()
    for d  in decisions:
        states.update(d['state'])

    cols = sorted(states)
    data = []
    for d in decisions:

        action = d['action']

        rw = [action]
        for c in cols:
            rw.append(d['state'][c])

        data.append(rw)


    r.table('decisions', data=data, rows=[''] * len(data),
            cols=['action'] + cols)


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

