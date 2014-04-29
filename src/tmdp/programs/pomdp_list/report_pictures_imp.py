from reprep import Report
from compmake.utils.describe import describe_value
from reprep.plot_utils.axes import turn_all_axes_off


def report_pictures(res, pomdp):
    trajectories = res['trajectories']

    r = Report()

    print(' I obtained %d trajectories' % len(trajectories))
    for i, tr in enumerate(trajectories):
        with r.subsection('tr%d' % i) as sub:
            report_pictures_trajectory(sub, res, pomdp, tr )

    return r


def report_pictures_trajectory(r, res, pomdp, tr):
    print describe_value(pomdp)
    beliefs = [tr[0]['belief']] + [t['belief2'] for t in tr]
    
    f = r.figure()

    for i, belief in enumerate(beliefs):
        
        with f.plot('t%s' % i) as pylab:
            pomdp.display_state_dist(pylab, belief)
            turn_all_axes_off(pylab)
#
        if i > 12: break
#         with r.subsection('t%s' % i) as sub:
#             sub.text('belief', str(belief))
#
