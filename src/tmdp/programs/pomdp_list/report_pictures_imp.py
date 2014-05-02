from collections import defaultdict
import os

from matplotlib.font_manager import FontProperties

import numpy as np
from procgraph_mplayer.quick_animation import pg_quick_animation
from reprep import Report
from reprep.plot_utils import turn_all_axes_off


def jobs_videos(context, res, pomdp):
    trajectories = res['trajectories']

    len2num = defaultdict(lambda:0)

    for i, tr in enumerate(trajectories):
        beliefs = [tr[0]['belief']] + [t['belief2'] for t in tr]
        agent_states = [tr[0]['agent_state']] + [t['agent_state'] for t in tr]

        ns = len(beliefs)
        # only creates one video per length of trajectory.
        if len2num[ns] > 0:
            continue

        len2num[ns] += 1

        out = os.path.join(context.get_output_dir(),
                           'tr-%03dsteps-%03d.mp4' % (ns, i))
        context.comp(video_trajectory, beliefs=beliefs,
                     agent_states=agent_states, pomdp=pomdp, out=out,
                     job_id='video%03d' % i)


def video_trajectory(beliefs, agent_states, pomdp, out,
                     video_params=dict(width=640, height=640, fps=15),
                     upsample=3, final_frames=15):
    nframes = len(beliefs) * upsample + final_frames

    def plotfunc(pylab, frame):
        frame = int(np.floor(frame / upsample))
        if frame >= len(beliefs):
            frame = len(beliefs) - 1

        belief = beliefs[frame]
        pomdp.display_state_dist(pylab, belief)

        agent_state = agent_states[frame]
        keys = sorted(agent_state.keys())
        values = [agent_state[k] for k in keys]
        state_string = ' '.join(map(str, values))
        pylab.figtext(0.1, 0.95 , state_string,
                      fontproperties=FontProperties(size=25))

        turn_all_axes_off(pylab)

    pg_quick_animation(plotfunc, nframes, out=out, **video_params)


def report_pictures(res, pomdp):
    trajectories = res['trajectories']

    r = Report()

    print(' I obtained %d trajectories' % len(trajectories))

    for i, tr in enumerate(trajectories):
        with r.subsection('tr%d' % i) as sub:
            report_pictures_trajectory(sub, res, pomdp, tr)

    return r


def report_pictures_trajectory(r, res, pomdp, tr):  # @UnusedVariable
#
#     beliefs = [tr[0]['belief']] + [t['belief2'] for t in tr]
#     nframes = len(beliefs)
#     def plotfunc(pylab, frame):
#         print('frame %d' % frame)
#         if frame >= len(beliefs):
#             frame = len(beliefs) - 1
#
#         belief = beliefs[frame]
#         pomdp.display_state_dist(pylab, belief)
#         turn_all_axes_off(pylab)
#
#     with r.data_file('animation', mime=MIME_MP4) as out:
#         pg_quick_animation(plotfunc, nframes, out=out, **video_params)


    f = r.figure()

    beliefs = [tr[0]['belief']] + [t['belief2'] for t in tr]

    for i, belief in enumerate(beliefs):
        with f.plot('t%s' % i) as pylab:
            pomdp.display_state_dist(pylab, belief)
            turn_all_axes_off(pylab)
#
#         if i > 12: break
#         with r.subsection('t%s' % i) as sub:
#             sub.text('belief', str(belief))
#
