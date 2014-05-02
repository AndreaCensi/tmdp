
src/tmdp/programs/pomdp_list/report_agent_imp.pyfrom reprep.utils.frozen import frozendict2
from reprep import Report
from contracts import contract
import numpy as np
# def create_agent(res, pomdp):
#     decisions_dis = res['decisions_dis']
#     trajectories = res['trajectories']
#
#     agent = create_agent(decisions_dis, trajectories)
#     check_agent(agent, trajectories)
#     res['agent'] = agent
#     return res


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

        data = []
        for state in states:
            row = [state[s] for s in self.states_names]
            data.append(row)

        r.table('states', data, cols=list(self.states_names))


        

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
