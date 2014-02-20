from abc import abstractmethod

from contracts import ContractsMeta, contract

from reprep import Report
from tmdp.mdp import SimpleMDP


__all__ = ['SimpleMDPSolver']


class SimpleMDPSolver():
    """ An object that can return a policy for a SimpleMDP. """
    
    __metaclass__ = ContractsMeta
    
    @abstractmethod
    @contract(mdp=SimpleMDP)
    def solve(self, mdp):
        """ Returns a dict with entries:
                 policy (state -> (a -> prob)) """
        pass

    @contract(r=Report, mdp=SimpleMDP, result=dict)
    def publish(self, r, mdp, result):  # @UnusedVariable
        """ 
            Return a report of the last computation. Result is the output
            of solve(). 
        """
        r.text('warn', 'Report not implemented.')


