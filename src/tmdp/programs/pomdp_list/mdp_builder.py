from collections import defaultdict

from contracts import contract

from tmdp.sampled_mdp import SampledMDP


__all__ = ['MDPBuilder']

class MDPBuilder():

    @contract(start_dist='ddist')
    def __init__(self, start_dist):

        self._state2id = {}
        self._id2state = {}
        self._transitions = []
        self.goals = set()

        self._start_dist = {}
        for state, p_state in start_dist.items():
            self._start_dist[self._get_id(state)] = float(p_state)

    def _get_id(self, state):
        if state in self._state2id:
            return self._state2id[state]
#         print('not creating different IDs')
#         l = len(self._state2id)
        l = state
        self._state2id[state] = l
        self._id2state[l] = state
        return l

    def mark_goal(self, state):
        self.goals.add(self._get_id(state))

    def add_state(self, state):
        pass

    def add_transition(self, state, action, state2, probability, reward):
        s1 = self._get_id(state)
        s2 = self._get_id(state2)
        t = (s1, action, s2, probability, reward)
        self._transitions.append(t)

    def get_sampled_mdp(self, goal_absorbing=True, stay=None):
        """ 
            If goal_absorbing = True, all actions of the goal states
            give the same state. 
        """

        state2actions = defaultdict(lambda: set())
        state2action2transition = defaultdict(lambda: defaultdict(lambda:{}))
        state2action2state2reward = \
            defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:{})))

        # create states self.states = set()
        states = set()
        for s1 in self._id2state:
            states.add(s1)

        actions = set()
        for (s1, action, s2, p, reward) in self._transitions:
            actions.add(action)
            state2actions[s1].add(action)
            state2action2transition[s1][action][s2] = float(p)  # += p
            state2action2state2reward[s1][action][s2] = reward  # += p

        if goal_absorbing:
            for g in self.goals:
                for a in actions:
                    state2actions[g].add(a)
                    state2action2transition[g][a][g] = 1.0
                    state2action2state2reward[g][a][g] = 0.0
        else:
            # for each goal state, we reset to the start distribution
            assert isinstance(stay, float)
            for g in self.goals:
                for a in actions:
                    state2actions[g].add(a)

                    state2action2transition[g][a] = {}
                    state2action2transition[g][a][g] = stay
                    state2action2state2reward[g][a][g] = 0.0
                    for s0 in self._start_dist:
                        x = self._start_dist[s0] * (1.0 - stay)
                        state2action2transition[g][a][s0] = x
                        state2action2state2reward[g][a][s0] = 0.0


        mdp = SampledMDP(states=states,
                         state2actions=state2actions,
                         state2action2transition=state2action2transition,
                         state2action2state2reward=state2action2state2reward,
                         start_dist=self._start_dist,
                         goals=self.goals)
        return mdp
