from contextlib import contextmanager
from itertools import product

from contracts import contract
from matplotlib.patches import Rectangle, Circle

from gridworld.grid_world import GridGeometry
import numpy as np
from reprep.graphics.filter_colormap import filter_colormap


@contextmanager
@contract(grid=GridGeometry)
def _display_map(grid, goal, pylab, fill_empty=True):
    gridmap = grid.get_map()
    H, W = gridmap.shape
    a = pylab.gca()

    a.add_patch(Rectangle((0, 0), H, W, edgecolor='black'))

    gg = GridGeometry(gridmap)

    _display_obstacles(pylab, gg)

    for (i, j) in product(range(H), range(W)):
        if gg.is_empty((i, j)):
            if fill_empty:
                fc = 'white'
            else:
                continue

            attrs = dict(fc=fc, ec='black')
            a.add_patch(Rectangle((i, j), 1, 1, **attrs))
        else:
            # attrs = dict(fc=obstacle_fill, ec='white')
            continue

    yield pylab

    for g in goal:
        a.add_patch(Rectangle(g, 1, 1, ec='blue', fc='none'))

    pylab.axis((-1, H + 1, -1, W + 1))
    pylab.axis('equal')

gray = '808080'
light_brown = '#E0D6A6'

@contract(gg=GridGeometry)
def _display_obstacles(pylab, gg, obstacle_fill=light_brown):
    a = pylab.gca()
    H, W = gg.get_map().shape
#     attrs = dict(fc=obstacle_fill, ec='none')
    a.add_patch(Rectangle((0, 0), H, W, ec='black', fc='none'))

    for (i, j) in product(range(H), range(W)):
        if gg.is_empty((i, j)):
            continue
        attrs = dict(fc=obstacle_fill, ec='none')
        a.add_patch(Rectangle((i, j), 1, 1, **attrs))

    

def _display_cell(pylab, state, **attrs):
    a = pylab.gca()
    i, j = state
    a.add_patch(Rectangle((i, j), 1, 1, **attrs))


@contract(grid=GridGeometry)
def _display_cell_action(grid, pylab, s, a, p_a):
    s2 = grid.next_cell(s, a)

    if False:
        e = p_a * 0.9
        d0 = (s2[0] - s[0]) * e
        d1 = (s2[1] - s[1]) * e

        if e > 0.3:
            head_width = 0.15
        else:
            head_width = 0
        pylab.arrow(s[0] + 0.5, s[1] + 0.5, d0, d1, ec='black', lw=0.15,
                    shape='full', head_width=head_width, length_includes_head=True)
    else:
        e = p_a * 0.45
        d0 = (s2[0] - s[0]) * e
        d1 = (s2[1] - s[1]) * e

        if e > 0.01:
            head_width = 0
            pylab.arrow(s[0] + 0.5, s[1] + 0.5, d0, d1, ec='black', lw=0.15,
                        shape='full', head_width=head_width, length_includes_head=True)

@contract(grid=GridGeometry)
def display_policy(grid, goal, pylab, policy, a_to_motion):
    """ Displays a policy (map from states to P(actions)). 
        a_to_motion: maps actions to arrows
    """
    with _display_map(grid, goal, pylab):
        for s, prob_a in policy.items():
            for a, p_a in prob_a.items():
                motion = a_to_motion(a)
                _display_cell_action(grid, pylab, s, motion, p_a)


@contract(grid=GridGeometry)
def display_state_values(grid, goal, pylab, state_values):
    values = np.array(state_values.values())
    m = values.min()
    M = values.max()
    norm = lambda x: (x - m) / (M - m)

    with _display_map(grid, goal, pylab):
        for s, v in state_values.items():
            fc = [norm(v), norm(v), norm(v)]
            _display_cell(pylab, s, fc=fc)


@contract(grid=GridGeometry)
def display_state_dist(grid, goal, pylab, state_dist, **kwargs):
    with _display_map(grid, goal, pylab):
        display_state_dist_only(pylab, state_dist, **kwargs)
        
def display_state_dist_only(pylab, state_dist, c1=[.8, .8, .8], c2=[0, 1, 0], ec='green'):
    c1 = np.array(c1)
    c2 = np.array(c2)
    max_p = max(state_dist.values())
    min_p = min(state_dist.values())
    for (i, j), p  in state_dist.items():
        if max_p == min_p:  # when all the probs are the same
            p = p
        else:
            p = p / max_p
        color = c1 * (1 - p) + c2 * p
        _display_cell(pylab, (i, j), fc=color, ec=ec)
    

@contract(grid=GridGeometry)
def display_neigh_field_value(grid, pylab, neig_values, marker_radius=0.2):
    values = np.abs(np.array(neig_values.values()))
    
    with _display_map(grid, [], pylab):
        a = pylab.gca()
        for (s1, s2), V in neig_values.items():
            s1 = np.array(s1)
            s2 = np.array(s2)
            p = (s1 + s2) / 2.0 + np.array([0.5, 0.5])
            ec = 'black'
            if values.max() > 0:
                c = -V / values.max()
            else:
                c = -V
            fc = [c, c, c]
            if V == 0:
                continue
            a.add_patch(Circle((p[0], p[1]), radius=marker_radius, fc=fc, ec=ec))



@contract(grid=GridGeometry, res='float,>0')
def display_sf_field_cont(grid, pylab, sf, res=0.5):

    shape = grid.get_map().shape
    xb = np.linspace(0, shape[0] * 1.0, shape[0] / res)
    yb = np.linspace(0, shape[1] * 1.0, shape[1] / res)
    X, Y = np.meshgrid(xb, yb)
    print('query...')
    values = sf.querygrid(X, Y)
    values = np.flipud(values)
    print('ocolormap')
    values_rgb = filter_colormap(values, cmap='jet')
    
    """ display continuous values """
    # with _display_map(grid, [], pylab, fill_empty=False):
    pylab.imshow(values_rgb, extent=(xb[0], xb[-1], yb[0], yb[-1]))
    _display_obstacles(pylab, grid)
