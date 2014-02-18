from collections import defaultdict

from contracts import contract

import numpy as np
from quickapp import CompmakeContext, QuickApp, iterate_context_names
from reprep import Report
from tmdp import get_conftools_tmdp_smdps
from tmdp.slice_sampling import slice_sampler
from tmdp.solving.free_energy import free_energy_iteration
from tmdp.solving.main import TMDP
from tmdp.solving.value_iteration_meat import vit_solve, policy_from_value


__all__ = ['VitSolve']


class VitSolve(TMDP.get_sub(), QuickApp):
    """ Run the main code. """

    cmd = 'vit-solve'

    def define_options(self, params):
        params.add_string_list('mdps', help='MDPS')

    @contract(context=CompmakeContext)
    def define_jobs_context(self, context):
        options = self.get_options()

        config_mdps = get_conftools_tmdp_smdps()
        id_mdps = config_mdps.expand_names(options.mdps)

        for cc, id_mdp in iterate_context_names(context, id_mdps):
            cc.add_extra_report_keys(id_mdp=id_mdp)

            # jobs_vit_display(cc, id_mdp)
            jobs_vit_solve(cc, id_mdp)

        context.create_dynamic_index_job()


def jobs_vit_display(context, id_mdp):
    config_smdps = get_conftools_tmdp_smdps()
    mdp = config_smdps.instance(id_mdp)
    r = context.comp_config(report_mdp_display, mdp)
    context.add_report(r, 'report_mdp_display')

def report_mdp_display(mdp):
    states = list(mdp.states())
    actions = list(mdp.actions())
    p = {states[0]: 1.0}

    N = 10
    plan = [actions[j] for j in np.random.randint(0, len(actions) - 1, N)]
    
    r = Report()
    f = r.figure()
    for i, a in enumerate(plan):
        with f.plot('p%d' % i) as pylab:
            mdp.display_state_dist(pylab, p)
        p = mdp.evolve(p, a)

    return r

def jobs_vit_solve(context, id_mdp):
    config_smdps = get_conftools_tmdp_smdps()
    mdp = config_smdps.instance(id_mdp)
    vit_res = context.comp(vit_solve, mdp, gamma=1.0)
    context.add_report(context.comp(report_vit, mdp, vit_res), 'vit')
    context.add_report(context.comp(report_policy, mdp, vit_res), 'policy')

    betas = [0.001, 0.05, 0.051, 0.052, 0.15, 0.5, 5]
    its = [10, 75, 75, 100, 75, 75, 50]
    for i, (c, beta) in enumerate(iterate_context_names(context, betas)):
        c.add_extra_report_keys(beta=beta)
        iterations = its[i]
        fe_res = c.comp(free_energy_iteration, mdp, min_iterations=iterations, max_iterations=iterations,
                         beta=beta)
        c.add_report(c.comp(report_free_energy, mdp, fe_res), 'report_free_energy')

def report_free_energy(mdp, fe_res):
    iterations = fe_res['iterations']
    last = iterations[-1]

    r = Report()
    r.text('params', str(fe_res['params']))

    policy = last['pi']
    report_maze_policy(r, mdp, policy)

    f = r.figure()
    with f.plot('z') as pylab:
        Z = last['Z']
        Zs = np.array(sorted(Z.values()))
        Zs = Zs / np.max(Zs)
        print('normlized: %s' % Zs)

        mdp.display_state_values(pylab, Z)
    return r

def report_maze_policy(r, mdp, policy):
    f = r.figure()
    with f.plot('policy') as pylab:

        mdp.display_policy(pylab, policy)

    state_dist = run_trajectories(mdp, start=(2, 2), policy=policy,
                                  nsteps=1000, ntraj=100,
                                  stop_at=(11, 11))
    with f.plot('state_dist') as pylab:
        mdp.display_state_dist(pylab, state_dist)




def run_trajectories(mdp, start, policy, nsteps, ntraj, stop_at):
    """ Returns prob. dist over states. """
    ds = defaultdict(lambda:0)
    for _ in range(ntraj):
        states = run_trajectory(mdp, start, policy, nsteps, stop_at)
        if states[-1] != stop_at:
            continue
        for s in states:
            ds[s] += (1.0 / ntraj) * (1.0 / len(states))
    return dict(ds)

def run_trajectory(mdp, start, policy, nsteps, stop_at):
    state = start
    traj = []
    for _ in range(nsteps):
        traj.append(state)
        if state == stop_at:
            break
        action = sample_from_dist(policy[state])
        state2_dist = mdp.transition(state, action)
        state = sample_from_dist(state2_dist)
    return traj

def sample_from_dist(p):
    values = []
    probs = []
    for value, prob in p.items():
        values.append(value)
        probs.append(prob)


#     assert sum(probs) == 1

    res = slice_sampler(probs, N=1)
    r = values[res]
    assert r in p
    return r



def report_policy(mdp, vit_res):
    policy = policy_from_value(mdp, vit_res)

    r = Report()
    report_maze_policy(r, mdp, policy)
#     f = r.figure()
#     with f.plot('policy') as pylab:
#         mdp.display_policy(pylab, policy)
    return r

def report_vit(mdp, vit_res):
    r = Report()

    f = r.figure()
    with f.plot('value') as pylab:
        mdp.display_state_values(pylab, vit_res)
    return r



