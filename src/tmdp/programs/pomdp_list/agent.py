from reprep.utils.frozen import frozendict2
from reprep import Report
from contracts import contract
import numpy as np
from reprep.constants import MIME_PNG, MIME_PDF


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

        agent.process_observations(observations)
        obtained = agent.get_commands()

        if obtained != expected:
            print('--- failure at step %d' % i)
            print('expected %r' % expected)
            print('obtained %r' % obtained)
            raise ValueError()

        s['agent_state'] = agent.get_state()



class Agent():

    def __init__(self, states_names, decisions):
        self.states_names = states_names

        self.transitions = {}  # (state, obs) -> state
        self.commands = {}  # (state, obs) -> command

        def interpret(state, rep_action):
            assert '=' in rep_action
            comp, value = rep_action.split('=')
            value = int(value)
            assert comp in state

            next_state = dict(**state)
            next_state[comp] = value
            next_state = frozendict2(next_state)

            return next_state

        for decision in decisions:
            actions = decision['action']
            state = dict(decision['state'])
            # history = decision['history']
            obs = state['last']
            del state['last']
            state = frozendict2(state)

            if isinstance(actions, tuple):
                assert len(actions) == 2, "Otherwise more complicated"

                real_action = actions[0]
                rep_action = actions[1]
                next_state = interpret(state, rep_action)

                if next_state == state:
                    print('Found info action %s, %s, %s -> %s' %
                          (state, obs, str(actions), next_state))
                    print('But this transition does not work!')
                    raise ValueError()

            else:
                real_action = actions
                rep_action = None
                next_state = state

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

        f = r.figure()
        import networkx as nx
        # pos = nx.spectral_layout(G)
        with f.plot('G', figsize=(5, 5)) as pylab:  # @UnusedVariable
            # nx_draw_with_attrs(G, pos=pos, with_labels=True)
            nx.draw(G)

        d = nx.to_pydot(G)  # d is a pydot graph object, dot options can be easily set
        # attributes get converted from networkx,
        # use set methods to control dot attributes after creation

        f = r.figure()

        f.data('pydot1', d.create_pdf(), mime=MIME_PDF)
        f.data('pydot2', d.create_png(), mime=MIME_PNG)

        r.text("name2state", str(name2state))
        r.text("name2obs", str(name2obs))
        r.text("name2obsset", str(name2obsset))

        
    def create_transition_graph(self):
        """ Creates an nx graph for the agent's internal transitions. """
        import networkx as nx
        G = nx.DiGraph()
        
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

#         state_namer = Namer('$s_%d$')
#         obs_namer = Namer('$y_%d$')
#         obsset_namer = Namer('$Y_%d$')
#
        state_namer = Namer('s%d')
        obs_namer = Namer('y%d')
        obsset_namer = Namer('Y%d')
        
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

            obsset = tuple(map(obs_namer, obs_list))
            obsset_name = obsset_namer(obsset)
            label = obsset_name
            print ('%s -> %s with %s' % (s1, s2, label))
            G.add_edge(s1, s2)
#             G.edge[s1][s2]['edge_color'] = [0, 0, 0]
            G.edge[s1][s2]['label'] = label

        return dict(G=G, 
                    name2state=state_namer.get_name2ob(),
                    name2obs = obs_namer.get_name2ob(),
                    name2obsset=obsset_namer.get_name2ob(),)


    def get_state(self):
        return frozendict2(self.state)

    def reset(self):
        self.state = self.state0
        

    def process_observations(self, obs):
        key = (self.state, obs)

        if not key in self.transitions:
            print('Cannot find key %s\n%s' % key)

            for (s, o) in self.transitions:
                if s == self.state:
                    print('Found same state but obs %r' % (str(o)))

            for (s, o) in self.transitions:
                if o == obs:
                    print('Found  obs but state %s' % (str(s)))

            raise ValueError()

        self.command = self.commands[key]
        self.state = self.transitions[key]

    def get_commands(self):
        return self.command
