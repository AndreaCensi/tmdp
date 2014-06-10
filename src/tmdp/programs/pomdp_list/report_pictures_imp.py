from collections import defaultdict
import os

from matplotlib.font_manager import FontProperties

import numpy as np
from procgraph_mplayer import pg_quick_animation
from reprep import Report
from reprep.plot_utils import turn_all_axes_off


def jobs_videos(context, res, pomdp, outdir, prefix, maxvideos=6):
    """ 
        Creates video jobs for representative sample of trajectories. 
    
        Returns
            d = res['videos'][i]
            
            d['filename'], d['traj']
              
    """
    trajectories = res['trajectories']

    len2num = defaultdict(lambda:0)
    
    res = {'videos': []}
    for i, tr in enumerate(trajectories):
        beliefs = [tr[0]['belief']] + [t['belief2'] for t in tr]
        agent_states = [tr[0]['agent_state']] + [t['agent_state'] for t in tr]

        # number of steps
        ns = len(beliefs)
        if len(trajectories) > maxvideos:

            # only creates one video per length of trajectory.
            if len2num[ns] > 0:
                continue

            len2num[ns] += 1

        trjname = 'tr%03dsteps%03d' % (ns, i)
        filename = '%s-%s.mp4' % (prefix, trjname)
        out = os.path.join(outdir, filename)
        filename = context.comp(video_trajectory, beliefs=beliefs,
                     agent_states=agent_states, pomdp=pomdp, out=out,
                     job_id='video-%s' % trjname)

        res['videos'].append(dict(filename=filename, traj=i))

        c2 = context.child(trjname)
        c2.add_extra_report_keys(trajectory=trjname)
        r = c2.comp(report_trajectory, beliefs, agent_states, pomdp)
        c2.add_report(r, 'trajectory')
    
    return res

def report_trajectory(beliefs, agent_states, pomdp):
    r = Report()

    plotter = TrajPlotter(beliefs=beliefs, pomdp=pomdp, agent_states=agent_states,
                          upsample=1)
    plotfunc = plotter.plotfunc
    
    f = r.figure(cols=8)

    x0, x1, y0, y1 = plotter.get_data_bounds()
    width = x1 - x0
    height = y1 - y0
    C = 0.4
    figsize = (C * width, C * height)

    for i in range(len(beliefs)):
        with f.plot('t%03d' % i, figsize=figsize) as pylab:
            plotfunc(pylab, i)
    return r


class TrajPlotter():
    def __init__(self, beliefs, pomdp, agent_states, upsample):
        self.beliefs = beliefs
        self.pomdp = pomdp
        self.agent_states = agent_states
        self.upsample = upsample


    def plotfunc(self, pylab, frame):
        turn_all_axes_off(pylab)

        frame = int(np.floor(frame / self.upsample))
        if frame >= len(self.beliefs):
            frame = len(self.beliefs) - 1

        belief = self.beliefs[frame]
        self.pomdp.display_state_dist(pylab, belief)

        agent_state = self.agent_states[frame]
        keys = sorted(agent_state.keys())
        values = [agent_state[k] for k in keys]
        state_string = ' '.join(map(str, values))

        #   pylab.figtext(0.1, 0.95 , state_string,
        #     fontproperties=FontProperties(size=25))

        max_len = 16
        size0 = 24 * 1.5
        if len(state_string) > max_len:
            use_len = size0 * max_len * 1.0 / len(state_string)
        else:
            use_len = size0

        shape = self.pomdp.get_grid_shape()
        dx = 0
        dy = shape[1] + 0.5
        pylab.text(dx, dy , state_string,
                   fontproperties=FontProperties(size=use_len))

        pylab.axis(self.get_data_bounds())

        pylab.tight_layout()

    def get_data_bounds(self):
        shape = self.pomdp.get_grid_shape()
        M = 0.33
        bounds = (-M, shape[0] + M, -M, shape[1] + 1 + M)
        return bounds


def video_trajectory(beliefs, agent_states, pomdp, out,
                     video_params=dict(width=640, height=640, fps=15),
                     upsample=3, final_frames=15):
    nframes = len(beliefs) * upsample + final_frames
    plotter = TrajPlotter(beliefs=beliefs, pomdp=pomdp, agent_states=agent_states,
                          upsample=upsample)
    plotfunc = plotter.plotfunc
    pg_quick_animation(plotfunc, nframes, out=out, **video_params)
    return out
#
# def report_pictures(res, pomdp):
#     trajectories = res['trajectories']
#
#     r = Report()
#
#     print(' I obtained %d trajectories' % len(trajectories))
#
#     for i, tr in enumerate(trajectories):
#         with r.subsection('tr%d' % i) as sub:
#             report_pictures_trajectory(sub, res, pomdp, tr)
#
#     return r

#
# def report_pictures_trajectory(r, res, pomdp, tr):  # @UnusedVariable
#
#     f = r.figure()
#
#     beliefs = [tr[0]['belief']] + [t['belief2'] for t in tr]
#
#     for i, belief in enumerate(beliefs):
#         with f.plot('t%s' % i) as pylab:
#             pomdp.display_state_dist(pylab, belief)
#             turn_all_axes_off(pylab)

