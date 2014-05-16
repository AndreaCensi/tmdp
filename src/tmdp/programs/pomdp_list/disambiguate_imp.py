from contracts import contract
from copy import deepcopy
import itertools
import os
from collections import defaultdict


@contract(decisions='set(dict)')
def disambiguate(decisions):
    """ 
        decisions = list of dicts with fields action, 
        state=dict(last=y) and history=tuple
    """
    
    # find the shortest ambiguous sequence. ambiguous means 
    # the state is the same but the action is different
    
    extra_states = []

    while True:


        """ REturns None or     (state, (d1, d2), (a1, a2)), l """
        res = find_shortest_ambiguous(decisions)

#         d0 = find_shortest_ambiguous(decisions)
        if res is None:
            print('Done! no ambiguous states; added %s bits.' % len(extra_states))
            return extra_states, decisions

        if False:
            (state, (d0, d1), (a0, a1)), prefix_len = res

        else:
            d0 = find_shortest_ambiguous_old(decisions)
            state = d0['state']
            amb = get_ambiguous_states(decisions, d0)
            amb.add(d0)
            assert len(amb) >= 2
            ((d0, d1), (a0, a1)), prefix_len = choose_decisions_to_disambiguate(amb)

#         # print('shortest: %s' % d0)
#         amb = get_ambiguous_states(decisions, d0)
#
#         assert len(amb) >= 1, decisions
#         # print('its siblings:')
#         # for i, x in enumerate(amb):
#         #    print(' ambiguous %d: %s' % (i, x))
#
#         # Ambiguous set of length >= 2
#         amb.add(d0)
#         assert len(amb) >= 2
#
#         ((d1_, d2_), (a1_, a2_)), prefix_len = choose_decisions_to_disambiguate(amb)
        print('Chosen ambiguous context %s ' % state)
        print('The best commands to disambiguate (l=%s) are "%s" and "%s".' %
               ((prefix_len, a0, a1)))
        print(' d0 history: %s' % str(d0['history']))
        print(' d1 history: %s' % str(d1['history']))

#         if False:
#             # how we did it before
#             amb_sorted = sorted(amb, key=lambda x: len(x['history']))
#             d0 = amb_sorted[0]
#             d1 = amb_sorted[1]
#         else:
#             d0 = d1_
#             d1 = d2_

        # should have the same state
        assert d0['state'] == d1['state']
        # ... different action
        assert d0['action'] != d1['action']
        # ... and be a subset
        h0 = d0['history']
        h1 = d1['history']
        
        assert is_prefix(h0[:prefix_len], h1[:prefix_len])
        # XXX: this might overflow...
        # assert not is_prefix(h0[:prefix_len + 1], h1[:prefix_len + 1])
        # print ('prefix[:len]= %s' % is_prefix(h0[:prefix_len], h1[:prefix_len]))
        # print ('prefix[:len+1]= %s' % is_prefix(h0[:prefix_len + 1], h1[:prefix_len + 1]))
        # print ('prefix[:len-1]= %s' % is_prefix(h0[:prefix_len - 1], h1[:prefix_len - 1]))

        if False:
            assert is_prefix(h0, h1)
            trigger = h1[:len(h0) + 1]
        else:
            trigger = h1[:prefix_len + 1]

        k = len(extra_states)
        # state_name = 's' + ['A', 'B', 'C', 'D', 'E', 'F', 'G'][k]
        state_name = 's%d' % k
        extra_states.append(dict(name=state_name, trigger=trigger))

        print('adding triggering condition of length %s' % len(trigger))
        print('trigger: %s' % str(trigger))

        decisions = add_state(decisions, name=state_name, trigger=trigger)
        
    assert False


def choose_decisions_to_disambiguate(amb):
    """ Returns d0, d1 """
    # amb: ambiguous decisions
    assert len(amb) >= 2
    # These are the commands
    actions = set([x['action'] for x in amb])
    assert len(actions) >= 2
    print('Ambiguous set: %d; ncommands: %s' % (len(amb), len(actions)))

    
    def decisions_for(a):
        return [d for d in amb if d['action'] == a]
    def goodness(a1, a2):
        assert a1 != a2
        # find decisions for each command
        dchoices = []  # (d1, d2)
        for d1, d2 in itertools.product(decisions_for(a1), decisions_for(a2)):
            assert d1['action'] != d2['action']
            assert d1['action'] == a1
            assert d2['action'] == a2
            dfactor = length_first_divergence(d1, d2)
            dchoices.append(((d1, d2), dfactor))
        (d1o, d2o), l = min(dchoices, key=lambda x:x[1])
        return (d1o, d2o), l

    choices = []  # (choice, factor)
    for a1, a2 in itertools.combinations(actions, 2):
        assert a1 != a2
        (d1, d2), factor = goodness(a1, a2)

        choice = (d1, d2), (a1, a2)
        choices.append((choice, factor))

    ((d1, d2), (a1, a2)), l = min(choices, key=lambda x:x[1])
    # print('Results for commands')
    # print(choices)
    return ((d1, d2), (a1, a2)), l

def length_first_divergence(d1, d2):
    h1 = d1['history']
    h2 = d2['history']

    cprefix = os.path.commonprefix([h1, h2])
    return len(cprefix)


def add_state(decisions, name, trigger):
    res = set()
    for d in deepcopy(decisions):
        history = d['history']
        if is_prefix(trigger, history):

            if history == trigger:
                d['action'] = (d['action'], '%s=%s' % (name, 1))

            # The action acts after one step
            if len(history) > len(trigger):
                value = 1
            else:
                value = 0
        else:
            value = 0
        assert not name in d['state']


        d['state'][name] = value
        res.add(d)
    return res


def is_prefix(h0, h1):
    """
        Checks that h0 is a prefix of h1.
    """
    if len(h0) > len(h1):
        return False
    for i, a in enumerate(h0):
        if a != h1[i]:
            return False
    return True

    
def get_ambiguous_states(decisions, d):
    """ Returns a set of ambiguous decisions for d """
    amb = set()
    for d2 in decisions:
        if d2 == d: continue
        same_state = d2['state'] == d['state']
        different_action = d2['action'] != d['action']
        if same_state and different_action:
            amb.add(d2)
    return amb 
    
def find_shortest_ambiguous(decisions):
    """ REturns None or     (state, (d1, d2), (a1, a2)), l """
    decisions = list(decisions)
    state2ambiguousdec = defaultdict(lambda: set())

    for d in decisions:
        ambs = get_ambiguous_states(decisions, d)
        if ambs:
            state2ambiguousdec[d['state']].add(d)
    
    if len(state2ambiguousdec) == 0:
        return None

    choices = [] 
    for state, amb_decisions in  state2ambiguousdec.items():
        ((d1_, d2_), (a1_, a2_)), prefix_len = choose_decisions_to_disambiguate(amb_decisions)
        choice = (state, (d1_, d2_), (a1_, a2_))
        choices.append((choice, prefix_len))

    (state, (d1, d2), (a1, a2)), l = min(choices, key=lambda x:x[1])
    # print('Results for commands')
    # print(choices)
    return (state, (d1, d2), (a1, a2)), l
#
#     length = lambda x: length_ambiguation(decisions, x)
#     ambiguous_sorted = sorted(ambiguous, key=length)
#
#     if ambiguous_sorted:
#         return ambiguous_sorted[0]
#     else:
#         return None


def find_shortest_ambiguous_old(decisions):
    decisions = list(decisions)
    ambiguous = set()
    for d in decisions:
        ambs = get_ambiguous_states(decisions, d)
        if ambs:
            ambiguous.add(d)

    length = lambda x: length_ambiguation(decisions, x)
    ambiguous_sorted = sorted(ambiguous, key=length)

    if ambiguous_sorted:
        return ambiguous_sorted[0]
    else:
        return None


def length_ambiguation(decisions, d):
    amb = get_ambiguous_states(decisions, d)
    if not amb:
        msg = 'Is this decision not ambiguous?\n'
        msg += 'd: %s\n' % d
        msg += 'amb: %s\n' % amb
        raise ValueError(msg)

    amb.add(d)
    lengths = sorted([len(d2['history']) for d2 in amb])
    length = lengths[1] - lengths[0]
    return length

    
    
