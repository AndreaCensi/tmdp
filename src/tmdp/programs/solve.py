from contracts import contract

from quickapp import CompmakeContext, QuickApp, iterate_context_names
from reprep import Report
from tmdp import get_conftools_tmdp_smdps
from tmdp.configuration import get_conftools_tmdp_smdp_solvers

from .main import TMDP


__all__ = ['Solve']


class Solve(TMDP.get_sub(), QuickApp):
    """ Solves a bunch of MDPs with the given solvers """

    cmd = 'solve'

    def define_options(self, params):
        params.add_string_list('mdps', help='MDPS')
        params.add_string_list('solvers', help='MDPSolvers')

    @contract(context=CompmakeContext)
    def define_jobs_context(self, context):
        options = self.get_options()

        config_mdps = get_conftools_tmdp_smdps()
        id_mdps = config_mdps.expand_names(options.mdps)

        config_solvers = get_conftools_tmdp_smdp_solvers()
        id_solvers = config_solvers.expand_names(options.solvers)
        
        for c2, id_mdp in iterate_context_names(context, id_mdps):
            c2.add_extra_report_keys(id_mdp=id_mdp)

            mdp = c2.comp_config(instance_mdp, id_mdp)

            from tmdp.programs.value_iteration import report_mdp_display
            r = c2.comp_config(report_mdp_display, mdp)
            c2.add_report(r, 'report_mdp_display')

            for cc, id_solver in iterate_context_names(c2, id_solvers):
                cc.add_extra_report_keys(id_solver=id_solver)
                jobs_solve(cc, mdp, id_solver)




def jobs_solve(context, mdp, id_solver):
    # We make a job out of these in case it needs to have a
    # bit of preprocessing.

    solver = context.comp_config(instance_solver, id_solver)
    result = context.comp(solve, mdp, solver)

    r = context.comp(report_solver, solver, mdp, result)
    context.add_report(r, 'report_solver')

    r = context.comp(report_policy, mdp, result)
    context.add_report(r, 'report_policy')
    
    return result

def report_policy(mdp, result):
    policy = result['policy']
    r = Report()
    from tmdp.programs.value_iteration import report_maze_policy
    report_maze_policy(r, mdp, policy)
    return r
    
def report_solver(solver, mdp, result):
    r = Report()
    solver.publish(r, mdp, result)
    return r

def solve(mdp, solver):
    result = solver.solve(mdp)
    return result

def instance_solver(id_solver):
    config = get_conftools_tmdp_smdp_solvers()
    return config.instance(id_solver)

def instance_mdp(id_mdp):
    config_smdps = get_conftools_tmdp_smdps()
    mdp = config_smdps.instance(id_mdp)
    return mdp

