from reprep import Report
from reprep.plot_utils.axes import turn_all_axes_off


def report_agent(res, pomdp):
    agent = res['agent']


    r = Report()

    f = r.figure()

    p_p0 = pomdp.get_start_dist_dist()
    for i, (p0, _) in enumerate(p_p0.items()):
        with f.plot('p0-%d' % i) as pylab:
            pomdp.display_state_dist(pylab, p0)
            turn_all_axes_off(pylab)

    with r.subsection('states') as sub:
        agent.report_states(sub)

    with r.subsection('transitions') as sub:
        agent.report_transitions(sub)


    return r
