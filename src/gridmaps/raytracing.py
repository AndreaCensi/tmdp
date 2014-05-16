
import numpy as np


__all__ = [ 'lineofsight']

def lineofsight(gridmap, cell1, cell2):
    """ No ostacles between center if cell1 and any corner of cell2. """
    cell1 = tuple(cell1)
    cell2 = tuple(cell2)
    def center_of(c):
        return np.array([c[0] + 0.5, c[1] + 0.5])

    def corners_of(c):
        c0 = np.array([c[0], c[1]], dtype='float')
        c1 = c0 + [0, 1]
        c2 = c0 + [1, 0]
        c3 = c0 + [1, 1]
        return [c0, c1, c2, c3]

    def unoccluded(p0, p1, c1, c2):
        trace = set(my_trace_path(p0, p1))
        if c1 in trace:
            trace.remove(c1)
        if c2 in trace:
            trace.remove(c2)
        obstacles = gridmap.get_wall_cells()
        occluded = set(trace) & set(obstacles)
        un = not bool(occluded)

#         print('%s -> %s ? %s  (%s)' % (p0, p1, un, trace))
        return un

    def my_trace_path(a, b):
        n = np.max(np.abs(a - b))
        n = n * 3
        ps = []
        EPS = 0.01
        for alpha in np.linspace(0.0 + EPS, 1.0 - EPS, n):
            p = np.floor(a * alpha + (1 - alpha) * b)
            p = (int(p[0]), int(p[1]))
            if not ps or ps[-1] != p:
                ps.append(p)
        return list(ps)

    u = [ unoccluded(center_of(cell1), p1, cell1, cell2)
         for p1 in corners_of(cell2) ]
    return np.any(u)
