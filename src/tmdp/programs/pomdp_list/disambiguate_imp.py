from contracts import contract
from copy import deepcopy


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
        d0 = find_shortest_ambiguous(decisions)
        if d0 is None:
            print('Done! no ambiguous states.')
            return extra_states, decisions

        print('shortest: %s' % d0)
        print('its siblings:')
        amb = get_ambiguous_states(decisions, d0)
        for x in amb:
            print x

        # ok, now find the second longest
        amb.add(d0)
        amb_sorted = sorted(amb, key=lambda x: len(x['history']))
        d0 = amb_sorted[0]
        d1 = amb_sorted[1]

        # should have the same state
        assert d0['state'] == d1['state']
        # ... different action
        assert d0['action'] != d1['action']
        # ... and be a subset
        h0 = d0['history']
        h1 = d1['history']
        # this is true in imap4 but not imap6
        assert is_prefix(h0, h1)

        trigger = h1[:len(h0) + 1]
        k = len(extra_states)
        state_name = 's' + ['A', 'B', 'C', 'D', 'E', 'F', 'G'][k]
        extra_states.append(dict(name=state_name, trigger=trigger))

        print('adding triggering condition:')
        print('trigger: %s' % str(trigger))

        decisions = add_state(decisions, name=state_name, trigger=trigger)
        
    assert False

def add_state(decisions, name, trigger):
    res = set()
    for d in deepcopy(decisions):
        history = d['history']
        if is_prefix(trigger, history):
            value = 1
            if history == trigger:
                d['action'] = (d['action'], '%s=%s)' % (name, 1))
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
    ambiguous = set()
    for d in decisions:
        ambs = get_ambiguous_states(decisions, d)
        if ambs:
            ambiguous.add(d)

    # length = lambda d: len(d['history'])
    length = lambda x: length_ambiguation(decisions, x)
    ambiguous_sorted = sorted(ambiguous, key=length)

    if ambiguous_sorted:
        return ambiguous_sorted[0]
    else:
        return None


def length_ambiguation(decisions, d):
    amb = get_ambiguous_states(decisions, d)
    amb.add(d)
    lengths = sorted([len(d2['history']) for d2 in amb])
    length = lengths[1] - lengths[0]
    return length

    
    
