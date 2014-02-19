from abc import abstractmethod
from collections import defaultdict

from contracts import ContractsMeta, new_contract
from numpy.testing.utils import assert_allclose
from numpy.core.numeric import allclose


__all__ = ['SimpleMDP']


class SimpleMDP():
    __metaclass__ = ContractsMeta


    @new_contract
    def is_action(self, action):
        pass

    @new_contract
    def is_state(self, state):
        pass

    def is_state_dist(self, state_dist):
        for s in state_dist:
            self.is_state(s)
        p = sum(state_dist.values())
        if not allclose(p, 1.0):
            raise ValueError('PD sums to %f' % p)

        
    @abstractmethod
    def states(self):
        """ 
            Returns an iterable with states. States are small
            hashable objects (like tuples, strings, etc.). 
        """

    @abstractmethod
    def actions(self, state):
        pass
    
    @abstractmethod
    def transition(self, state, action):
        pass

    @abstractmethod
    def reward(self, state, action, state2):
        pass

    @abstractmethod
    def get_start_dist(self):
        """ Return the start distribution (episodic) """
        pass

    def evolve_actions(self, state_dist, actions):
        p = state_dist
        for a in actions:
            self.is_action(a)
            p = p.evolve(p, a)
        return p

    def evolve(self, state_dist, action):
        p2 = defaultdict(lambda:0.0)
        for s1, p_s1 in state_dist.items():
            conditional = self.transition(s1, action)
            self.is_state_dist(conditional)
            for s2, p_s2 in conditional.items():
                p2[s2] += p_s2 * p_s1
        return dict(**p2)

    # Debug
    @abstractmethod
    def display_state_dist(self, pylab, state_dist):
        """ 
            dist: hash states -> value >= 0 
        """
        pass

    @abstractmethod
    def display_state_values(self, pylab, state_values):
        pass

    @abstractmethod
    def display_policy(self, pylab, det_policy):
        pass

class SimplePOMDP(SimpleMDP):

    def get_observations(self):
        """ Returns a list of all possible observations. """
        pass

    def get_observations_dist(self, state):
        """ Returns the pd of observations given state. """




