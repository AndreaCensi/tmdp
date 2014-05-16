from contracts import contract

from quickapp import CompmakeContext, QuickApp, iterate_context_names
from tmdp import get_conftools_tmdp_smdps
from tmdp.programs.main import TMDP
from tmdp.programs.show import instance_mdp

from .meat import pomdp_list_states, find_minimal_policy
from .report_aliasing_imp import report_aliasing
from .report_pictures_imp import jobs_videos
from tmdp.programs.pomdp_list.report_agent_imp import report_agent
from tmdp.programs.pomdp_list.alternate_observations import alternate_observersations_an
from grid_intruder.intruder_pomdp import IntruderPOMDP
from grid_intruder.intruder_pomdp_rf import IntruderPOMDPrf


__all__ = ['POMDPList']


class POMDPList(TMDP.get_sub(), QuickApp):
    """ Lists all reachable states of the POMDP. """

    cmd = 'pomdp-list'

    def define_options(self, params):
        params.add_string_list('mdps', help='POMDPS')

    @contract(context=CompmakeContext)
    def define_jobs_context(self, context):
        options = self.get_options()

        context.activate_dynamic_reports()

        config_mdps = get_conftools_tmdp_smdps()
        id_mdps = config_mdps.expand_names(options.mdps)

        for cc, id_mdp in iterate_context_names(context, id_mdps):
            cc.add_extra_report_keys(id_mdp=id_mdp)
            pomdp = cc.comp_config(instance_mdp, id_mdp)

            res = cc.comp(pomdp_list_states, pomdp)
            """ Returns res['builder'] as a MDPBuilder """
            res = cc.comp(find_minimal_policy, res, pomdp)

            cc.add_report(cc.comp(report_agent, res, pomdp),
                          'report_agent')

            cc.add_report(cc.comp(report_aliasing, res, pomdp),
                          'report_aliasing')

            # Too long (too many states)
            # cc.add_report(cc.comp(report_sampled_mdp, res, pomdp),
            # 'sampled_mdp')

            # Too long (too many iterations)
            # cc.add_report(cc.comp(report_pictures, res, pomdp),
            # 'report_pictures')

            cc.comp_dynamic(jobs_videos, res, pomdp)

            # See if we can do the same policy with different
            # observation model
            horizons = [0, 1, 2, 3, 4]
            for ch, horizon in iterate_context_names(cc, horizons, key='horizon'):
                pomdp2 = ch.comp(get_alternative_pomdp, pomdp, horizon)
                res2 = ch.comp(alternate_observersations_an, res, pomdp, pomdp2)
                ch.add_report(ch.comp(report_agent, res2, pomdp, job_id='report_agent_z'),
                              'report_agent_z')
                ch.comp_dynamic(jobs_videos, res2, pomdp2)


def get_alternative_pomdp(pomdp, horizon):
    if not isinstance(pomdp, IntruderPOMDP):
        raise ValueError('Works only for IntruderPOMDP.')

    new_pomdp = IntruderPOMDPrf(pomdp.get_gridmap(), horizon=horizon)
    return new_pomdp

