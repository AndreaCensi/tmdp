import itertools

from contracts import contract
from decorator import decorator

from gridworld.drawing import display_sf_field_cont
import numpy as np
from quickapp import CompmakeContext, QuickApp, iterate_context_names
from reprep import Report
from reprep.plot_utils.axes import turn_all_axes_off
from tmdp import get_conftools_tmdp_smdp_solvers, get_conftools_tmdp_smdps

from .main import TMDP
from .show import instance_mdp
from .solve import jobs_solve
from .tension import get_tension_matrix


__all__ = ['StateDiff']


class StateDiff(TMDP.get_sub(), QuickApp):
    """ Displays some statistics of the solution. """

    cmd = 'state-diff'

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
                solve_result = jobs_solve(cc, mdp, id_solver)

                points = [100, 200, 500]
                for c3, num_points in iterate_context_names(cc, points):
                    c3.add_extra_report_keys(num_points=num_points)

                    res = c3.comp(resample, mdp, solve_result,
                                  num_points=num_points)

                    c3.add_report(c3.comp(report_resample, mdp, res),
                                  'report_resample')
                    c3.add_report(c3.comp(report_tension, mdp, res),
                                  'report_tension')



def resample(mdp, solve_result, num_points):
    policy = solve_result['policy']
    value = solve_result['value']
    tension = get_tension_matrix(mdp, policy, value)
    density = {a:-b for (a, b) in tension.items()}
    density_sf = sf_from_tension(density, alpha=1.5)

    support_points = mdp.get_support_points()
    
    shape = mdp.get_grid().get_map().shape
    grid = mdp.get_grid()
    def support():
        x = np.random.rand(2)
        return np.array([x[0] * shape[0], x[1] * shape[1]])
        
    def weight(p):
        cell = np.floor(p)
        cell = (int(cell[0]), int(cell[1]))
        empty = grid.is_empty(cell)
        if not empty:
            return 0
        d = density_sf.query(p)
        return d

    
    sampled_points = rejection_sampling(support=support,
                                        weight=weight, N=num_points)
    

    points = support_points + sampled_points
    from pyhull.delaunay import DelaunayTri
    delaunay_tri = DelaunayTri(points)
    print delaunay_tri.vertices
    print delaunay_tri.points


    solve_result['delaunay_tri'] = delaunay_tri
    solve_result['sampled_points'] = sampled_points
    solve_result['tension'] = tension
    solve_result['density_sf'] = density_sf
    solve_result['support_points'] = support_points
    return solve_result

@decorator
def aslist(f, *args, **kwargs):
    res = []
    for x in f(*args, **kwargs):
        res.append(x)
    return res

@aslist
def rejection_sampling(support, weight, N):
    n = 0
    while n < N:
        p = support()
        w = weight(p)
        if np.random.rand() > w:
            continue
        yield p
        n += 1

def report_resample(mdp, resample_res):  # @UnusedVariable
    support_points = resample_res['support_points']
    sampled_points = resample_res['sampled_points']
    delaunay_tri = resample_res['delaunay_tri']

    r = Report()
    f = r.figure()
    
    with f.plot('support') as pylab:

        for p in support_points:
            pylab.plot(p[0], p[1], 'kx')

        for p in sampled_points:
            pylab.plot(p[0], p[1], 'rx')

    with f.plot('triangulation') as pylab:
        plot_triangulation(pylab, delaunay_tri)

    with f.plot('both') as pylab:
        plot_triangulation(pylab, delaunay_tri)

        for p in  support_points:
            pylab.plot(p[0], p[1], 'kx')

        for p in sampled_points:
            pylab.plot(p[0], p[1], 'rx')

    return r


def plot_triangulation(pylab, tri):
    v = tri.vertices
    p = tri.points
    def line(p1, p2):
        pylab.plot([p1[0], p2[0]], [p1[1], p2[1]], '-')

    for (a, b, c) in v:
        line(p[a], p[b])
        line(p[a], p[c])
        line(p[c], p[b])


def report_tension(mdp, resample_res, resolution=0.33):
    tension = resample_res['tension']
    density_sf = resample_res['density_sf']

    r = Report()
    f = r.figure()

    with f.plot('tension1') as pylab:
        mdp.display_neigh_field_value(pylab, tension)
        turn_all_axes_off(pylab)

    with f.plot('density') as pylab:
        display_sf_field_cont(mdp.get_grid(), pylab,
                              density_sf, res=density_sf)
        turn_all_axes_off(pylab)
    return r


class SampledFunction():
    def __init__(self, kernel):
        self.kernel = kernel
        self.support = []
        self.values = []

    @contract(x='array', f_x='float')
    def add_sample(self, x, f_x):
        self.support.append(x)
        self.values.append(f_x)

    def query(self, x):
        q = np.array([self.kernel(x, x0) for x0 in self.support])
        q = q / np.sum(q)
        f = np.array(self.values)
        return np.sum(q * f)

    def __call__(self, x):
        return self.query(x)

    def querygrid(self, X, Y):
        res = np.empty_like(X)
        for i, j in iterate_indices(X.shape):
            p = np.array([X[i, j], Y[i, j]])
            res[i, j] = self.query(p)
        return res


def iterate_indices(shape):
    if len(shape) == 2:
        for i, j in itertools.product(range(shape[0]), range(shape[1])):
            yield i, j
    else:
        raise NotImplementedError
        assert(False)
        
class ExpKernel():
    def __init__(self, alpha):
        self.alpha = alpha
    def __call__(self, p1, p2):
        return np.exp(-self.alpha * np.linalg.norm(p1 - p2))


@contract(returns=SampledFunction)
def sf_from_tension(neig_values, alpha):
    kernel = ExpKernel(alpha)
    sf = SampledFunction(kernel=kernel)

    for (p1, p2), tension in neig_values.items():
        center = (np.array(p1) + np.array(p2)) / 2.0 + np.array([0.5, 0.5])
        value = tension
        sf.add_sample(center, value)

    return sf


