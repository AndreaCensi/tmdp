from contracts import contract

from quickapp import CompmakeContext, QuickApp, iterate_context_names
from reprep import Report
from tmdp import get_conftools_tmdp_smdps
from tmdp.mdp_utils.mdps_utils import all_actions, dist_evolve

from .main import TMDP


__all__ = ['MDPShow']


class MDPShow(TMDP.get_sub(), QuickApp):
    """ Displays some debug info about the MDP. """

    cmd = 'show'

    def define_options(self, params):
        params.add_string_list('mdps', help='MDPS')

    @contract(context=CompmakeContext)
    def define_jobs_context(self, context):
        options = self.get_options()

        config_mdps = get_conftools_tmdp_smdps()
        id_mdps = config_mdps.expand_names(options.mdps)

        for cc, id_mdp in iterate_context_names(context, id_mdps):
            cc.add_extra_report_keys(id_mdp=id_mdp)
            mdp = cc.comp_config(instance_mdp, id_mdp)

            cc.add_report(cc.comp(report_start_dist, mdp), 'start_dist')
            cc.add_report(cc.comp(report_actions, mdp), 'actions')

        context.create_dynamic_index_job()

def instance_mdp(id_mdp):
    config_smdps = get_conftools_tmdp_smdps()
    mdp = config_smdps.instance(id_mdp)
    return mdp

def report_start_dist(mdp):
    r = Report()
    f = r.figure()

    start = mdp.get_start_dist()
    with f.plot('start_dist', caption='Start distribution') as pylab:
        mdp.display_state_dist(pylab, start)

    return r


def report_actions(mdp):
    r = Report()
    f = r.figure()
    actions = all_actions(mdp)

    start = mdp.get_start_dist()

    for a in actions:
        f = r.figure()
        P = start
        for _ in range(4):
            conditional = dict((s, mdp.transition(s, a)) for s in P)
            P = dist_evolve(P, conditional)
        with f.plot('step1') as pylab:
            mdp.display_state_dist(pylab, P)
    return r







