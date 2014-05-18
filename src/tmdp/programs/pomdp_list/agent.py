from reprep.utils.frozen import frozendict2
from reprep import Report
from contracts import contract
import numpy as np
from reprep.constants import MIME_PNG, MIME_PDF
import pydot
import warnings


def create_agent(decisions_dis):
    states = list(list(decisions_dis)[0]['state'].keys())
    states.remove('last')
    decisions = decisions_dis
    agent = Agent(states_names=states, decisions=decisions)

    return agent

def check_agent(agent, trajectories):
    """ 
        Checks that the agent reconstructs the actions exactly;
        add field "agent_state".
    """
    for tr in trajectories:
        check_agent_trajectory(agent, tr)

def check_agent_trajectory(agent, tr):
    """"A trajectory is a sequence of dictionaries with fields
            dict(action=action, obs=y,
                belief=belief, belief1=belief1,
                 ydist=ydist, belief2=belief2)
        Checks that the agent reconstructs the actions exactly;
        add field "agent_state".
    """
    agent.reset()
    for i, s in enumerate(tr):
        observations = s['obs']
        expected = s['action']

        s['agent_state'] = agent.get_state()

        obtained = agent.get_commands(obs=observations)

        if obtained != expected:
            print('--- failure at step %d / %d' % (i + 1, len(tr)))
            print('expected %r' % str(expected))
            print('obtained %r' % str(obtained))
            raise ValueError()

        agent.update_state(observations)
        s['agent_state_next'] = agent.get_state()




def interpret_actions(state, action):
    """ actions =action or tuple(real_action, 's=1') 
        returns next_state, real action
    """
    warnings.warn('here we are assuming that commands are not tuple')
    assert isinstance(state, dict)
#     warnings.warn('here we are assuming that commands are string')
#     assert isinstance(action, (tuple, str))
    if isinstance(action, tuple):
        assert len(action) == 2
        action0, rep_action = action
#         print('unpacking %r in action0 = %r, rep_action = %r' % (action, action0, rep_action))
        assert '=' in rep_action
        next_state = interpret_actions_one(state, rep_action)
        return interpret_actions(next_state, action0)
    else:
        return state, action

def interpret_actions_one(state, rep_action):
    assert isinstance(state, dict), state
    assert isinstance(rep_action, str), rep_action
    assert '=' in rep_action, 'Invalid rep action %s (state %s)' % (rep_action, state)
    comp, value = rep_action.split('=')
    value = int(value)
    assert comp in state

    next_state = dict(**state)
    next_state[comp] = value
    next_state = frozendict2(next_state)

    return next_state


class Agent():

    def __init__(self, states_names, decisions):
        """ Note that the commands cannot be tuples. """
        self.states_names = states_names

        self.transitions = {}  # (state, obs) -> state
        self.commands = {}  # (state, obs) -> command


        for decision in decisions:
            actions = decision['action']
            state = dict(decision['state'])
            # history = decision['history']
            obs = state['last']
            del state['last']
            state = frozendict2(state)

            next_state, real_action = interpret_actions(state, actions)

#             warnings.warn('here we are assuming that commands are string')
#             assert isinstance(real_action, str)
            assert isinstance(next_state, dict)
#             
#             if isinstance(actions, tuple):
#                 assert len(actions) == 2, "Otherwise more complicated"
# 
#                 real_action = actions[0]
#                 assert not isinstance(real_action, tuple)
#                 rep_action = actions[1]
#                 next_state = interpret(state, rep_action)
# 
#                 if next_state == state:
#                     print('Found info action %s, %s, %s -> %s' %
#                           (state, obs, str(actions), next_state))
#                     print('But this transition does not work!')
#                     raise ValueError()
# 
#             else:
#                 real_action = actions
#                 rep_action = None
#                 next_state = state

            if state!=next_state:
                print('Transition %s, %s -> %s' % (state , obs, next_state))

            self.transitions[(state, obs)] = next_state
            self.commands[(state, obs)] = real_action


        self.state0 = frozendict2(dict([s, 0] for s in self.states_names)) 
        self.decisions = decisions


    def get_all_states(self):
        state0 = frozendict2(dict([s, 0] for s in self.states_names))
        states = set(self.transitions.values())
        states.add(state0)
        return states

    def get_num_states_components(self):
        return len(self.states_names)

    @contract(r=Report)
    def report_states(self, r):
        states = self.get_all_states()
        nbits = self.get_num_states_components()
        
        r.text('num_states', len(states))
        r.text('num_bits', nbits)
        eff = ((100.0 * len(states) / np.power(2, nbits)))
        r.text('efficiency', '%.2f%% ' % eff)

        if nbits > 0:
            data = []
            for state in states:
                row = [state[s] for s in self.states_names]
                data.append(row)

            r.table('states', data, cols=list(self.states_names))


    @contract(r=Report)
    def report_transitions(self, r):
        Gd = self.create_transition_graph()
        G = Gd['G']
        name2state = Gd['name2state']
        name2obs = Gd['name2obs']
        name2obsset = Gd['name2obsset']
        name2cmd = Gd['name2cmd']
        policy = Gd['policy']

#         f = r.figure()
        import networkx as nx
#         # pos = nx.spectral_layout(G)
#         with f.plot('G', figsize=(5, 5)) as pylab:  # @UnusedVariable
#             # nx_draw_with_attrs(G, pos=pos, with_labels=True)
#             nx.draw(G)

        d = nx.to_pydot(G)  # d is a pydot graph object, dot options can be easily set
        # attributes get converted from networkx,
        # use set methods to control dot attributes after creation

        f = r.figure()

        f.data('pydot1', d.create_pdf(), mime=MIME_PDF)
        f.data('pydot2', d.create_png(), mime=MIME_PNG)

        
        f = r.figure('policy')

        gpolicy = get_policy_graph(policy)
        f.data('pydot1', gpolicy.create_pdf(), mime=MIME_PDF)
        f.data('pydot2', gpolicy.create_png(), mime=MIME_PNG)


    
        r.text("name2state", str(name2state))
        r.text("name2obs", str(name2obs))
        r.text("name2obsset", str(name2obsset))
        r.text("name2cmd", str(name2cmd))
        
    def create_transition_graph(self):
        """ Creates an nx graph for the agent's internal transitions. """
        import networkx as nx
        G = nx.DiGraph()

#         state_namer = Namer('$s_%d$')
#         obs_namer = Namer('$y_%d$')
#         obsset_namer = Namer('$Y_%d$')
#
        state_namer = Namer('s%d')
        obs_namer = Namer('y%d')
        obsset_namer = Namer('Y%d')
        cmd_namer = Namer('u%d')
#         cmd_namer = lambda x: x
        # each state is a node
        for state in self.get_all_states():
            s = state_namer(state)
            G.add_node(s)
#             G.node[s]['node_size'] = 20
#             G.node[s]['node_color'] = [0, 0, 1]

        T = self.transitions  # (state, obs) -> state

        from collections import defaultdict
        edges = defaultdict(lambda: list())  # (s1,s2) -> obs1, obs2, ...

        for (state1, obs), state2 in T.items():
            edges[(state1, state2)].append(obs)

        for (state1, state2), obs_list in edges.items():
            s1 = state_namer(state1)
            s2 = state_namer(state2)

            obsset = tuple(sorted(map(obs_namer, obs_list)))
            obsset_name = obsset_namer(obsset)
            label = obsset_name
            print ('%s -> %s with %s' % (s1, s2, label))
            G.add_edge(s1, s2)
#             G.edge[s1][s2]['edge_color'] = [0, 0, 0]
            G.edge[s1][s2]['label'] = label


        
        # now for the commands
        #
        #
        C = self.commands  # (state, obs) -> command
        
        
        # (state, cmd) => obs1, ..., obs2
        # Which observations make the agent choose cmd in state?
        statecmd2obs = defaultdict(lambda: list())
        
        # print('iterating self.commands')
        for (state, obs), cmd in C.items():
            statecmd2obs[(state,cmd)].append(obs)
            # print('%s, %s -> %s' % (state, obs, cmd))

        # A compact representation of the policy
        # as a map from (state, set of observations) to commands.

        # policy: (state, obsset) -> cmd
        policy = {}
        # print('iterating statecmd2obs')
        for (state, cmd), obsset in statecmd2obs.items():
            # print(' %s, %s => %s' % (state, cmd, obsset))
            obsset = tuple(sorted(map(obs_namer, obsset)))
            obsset_name = obsset_namer(obsset)
            
            state_name = state_namer(state)
            cmd_name = cmd_namer(cmd)

            # print('  or %s, %s => %s' % (state_name, cmd_name, obsset_name))
            # print('  |because %s = %s' % (obsset_name, obsset))
            key = (state_name, obsset_name)
            # print('key', key)
            assert not key in policy
            warnings.warn('writing out commands instead of naming them')
            policy[key] = cmd_name
            policy[key] = cmd

        # print 'all commands', set(policy.values()), set(C.values())

        assert len(set(policy.values())) == len(set(C.values()))

        print policy

        for n, obsset in obsset_namer.get_name2ob().items():
            print('%4s is %3d obs: %s' % (n, len(obsset), obsset))

        for n, cmd in cmd_namer.get_name2ob().items():
            print('%4s is %s' % (n, cmd))

        return dict(G=G, 
                    name2state=state_namer.get_name2ob(),
                    name2obs = obs_namer.get_name2ob(),
                    name2cmd=cmd_namer.get_name2ob(),
                    name2obsset=obsset_namer.get_name2ob(),
                    policy=policy)


    def get_state(self):
        return frozendict2(self.state)

    def reset(self):
        self.state = self.state0
        
    def update_state(self, obs):
        key = (self.state, obs)

        if not key in self.transitions:
            msg = ('Cannot find context state %s, obs %s' % key)

            for (s, o) in self.transitions:
                if s == self.state:
                    msg += ('\nFound same state but obs %r' % (str(o)))

            for (s, o) in self.transitions:
                if o == obs:
                    msg += ('\nFound obs but state %s' % (str(s)))
            print msg
            raise ValueError(msg)

#         self.command = self.commands[key]
        self.state = self.transitions[key]

    def get_commands(self, obs):
        key = (self.state, obs)
        assert key in self.commands
        return self.commands[key]
#
#         cmd = self.command
#         # FIXME, in this case cmd = ('u', 's22=1'). We should have picked earlier.
#         if isinstance(cmd, tuple):
#             cmd = cmd[0]
#         return cmd

def get_policy_graph(policy):
    graph = pydot.Dot('ordered', graph_type='digraph', compound='true',
                      fontname='Times', fontsize=20)
    gcontexts = pydot.Cluster('context', rank='same', label='Contexts')
    gcommands = pydot.Cluster('commands', rank='same', label='Commands')
    graph.add_subgraph(gcommands)
    graph.add_subgraph(gcontexts)

    for cmd in set(policy.values()):
        gcommands.add_node(pydot.Node(cmd))


    stategroup = {}
    for (state, obsset), cmd in policy.items():
        if not state in stategroup:
            stategroup[state] = pydot.Cluster('state%s' % str(state), label=state)
            gcontexts.add_subgraph(stategroup[state])

    for (state, obsset), cmd in policy.items():
        n = '%s, %s' % (state, obsset)
        parent = gcontexts
        parent = stategroup[state]
        parent.add_node(pydot.Node(n, label=obsset))

#         graph.add_edge(pydot.Edge(n, cmd,
#                                       ltail=gcontexts.get_name(),
#                                       lhead=gcommands.get_name()))

        graph.add_edge(pydot.Edge(n, cmd))

    return graph


class Namer():
    def __init__(self, pattern):
        self.pattern = pattern
        self.ob2name = {}
    def __call__(self, ob):
        if not ob in  self.ob2name:
            self.ob2name[ob] = self.pattern % len(self.ob2name)
        return self.ob2name[ob]

    def get_name2ob(self):
        return dict((name, ob) for ob, name in self.ob2name.items())
