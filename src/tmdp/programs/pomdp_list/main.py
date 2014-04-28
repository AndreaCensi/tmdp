from contracts import contract

from quickapp import CompmakeContext, QuickApp, iterate_context_names
from tmdp import get_conftools_tmdp_smdps
from tmdp.programs.main import TMDP
from tmdp.programs.show import instance_mdp

from .meat import pomdp_list_states, find_minimal_policy
from .report_aliasing_imp import report_aliasing
from .reports import report_sampled_mdp


__all__ = ['POMDPList']

class POMDPList(TMDP.get_sub(), QuickApp):
    """ Lists all reachable states of the POMDP. """

    cmd = 'pomdp-list'

    def define_options(self, params):
        params.add_string_list('mdps', help='POMDPS')

    @contract(context=CompmakeContext)
    def define_jobs_context(self, context):
        options = self.get_options()

        config_mdps = get_conftools_tmdp_smdps()
        id_mdps = config_mdps.expand_names(options.mdps)

        for cc, id_mdp in iterate_context_names(context, id_mdps):
            cc.add_extra_report_keys(id_mdp=id_mdp)
            pomdp = cc.comp_config(instance_mdp, id_mdp)

            res = cc.comp(pomdp_list_states, pomdp)
            """ Returns res['builder'] as a MDPBuilder """
            res = cc.comp(find_minimal_policy, res)

            cc.add_report(cc.comp(report_sampled_mdp, res, pomdp), 'sampled_mdp')
            cc.add_report(cc.comp(report_aliasing, res, pomdp), 'report_aliasing')
