import os

import numpy as np
from procgraph_mplayer.quick_animation import pg_quick_animation
from reprep import Report
from reprep.plot_utils import turn_all_axes_off


def jobs_videos(context, res, pomdp):
    trajectories = res['trajectories']

    for i, tr in enumerate(trajectories):
        beliefs = [tr[0]['belief']] + [t['belief2'] for t in tr]
        ns = len(beliefs)
        out = os.path.join(context.get_output_dir(),
                           'tr-%03dsteps-%03d.mp4' % (ns, i))
        context.comp(video_trajectory, beliefs, pomdp, out,
                     job_id='video%03d' % i)


def video_trajectory(beliefs, pomdp, out,
                     video_params=dict(width=640, height=640, fps=15),
                     upsample=3):
    nframes = len(beliefs) * upsample

    def plotfunc(pylab, frame):
        frame = int(np.floor(frame / upsample))
        if frame >= len(beliefs):
            frame = len(beliefs) - 1

        belief = beliefs[frame]
        pomdp.display_state_dist(pylab, belief)
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
