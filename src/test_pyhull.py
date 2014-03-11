from pyhull.convex_hull import ConvexHull
from reprep import Report
import numpy as np





def main():
    c = np.array([0.4,0.1])
    alpha = 20

    def density(p):    
        dist = np.linalg.norm(p-c)
        f = np.exp(-alpha*dist)
        return f

    def rand_point():
        return np.random.rand(2)

    def rejection_sample():
        while True:
            point = rand_point()
            p_accept = density(point)
            if np.random.rand() < p_accept:
                return point

    n = 300
    pts = [rejection_sample() for _ in range(n)] + [[0,0],[0,1],[1,1],[1,0]]



    from pyhull.delaunay import DelaunayTri
    tri = DelaunayTri(pts)
    print tri.vertices
    [[2, 4, 0], [4, 1, 0], [3, 4, 2], [4, 3, 1]]
    print tri.points
    [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5], [0, 0]]
    from pyhull.voronoi import VoronoiTess
    v = VoronoiTess(pts)
    print v.vertices
    [[-10.101, -10.101], [0.0, -0.5], [-0.5, 0.0], [0.5, 0.0], [0.0, 0.5]]
    print v.regions
    [[2, 0, 1], [4, 0, 2], [3, 0, 1], [4, 0, 3], [4, 2, 1, 3]]


    r = Report()
    f = r.figure()
    with f.plot('myplot') as pylab:
        for p in pts:
            pylab.plot(p[0],p[1],'rx')
        plot_triangulation(pylab, tri)
        #plot_tesselation(pylab, v)
        m=0.2
        pylab.axis((-m,1+m,-m,1+m))


    r.to_html('test_pyhull.html')

def plot_triangulation(pylab, tri):
    v = tri.vertices
    p = tri.points
    def line(p1,p2):
        pylab.plot([p1[0],p2[0]],[p1[1],p2[1]], '-')

    for (a,b,c) in v:
        line(p[a], p[b])
        line(p[a], p[c])
        line(p[c], p[b])


def plot_tesselation(plt, tess):
    points = tess.points
    avg = np.average(points, 0)
    vertices = tess.vertices
    for nn, vind in tess.ridges.items():
        (i1, i2) = sorted(vind)
        if i1 == 0:
            c1 = np.array(vertices[i2])
            midpt = 0.5 * (np.array(points[nn[0]]) + np.array(points[nn[1]]))
            if np.dot(avg - midpt, c1 - midpt)> 0:
                c2 = c1 + 10 * (midpt-c1)
            else:
                c2 = c1 - 10 * (midpt-c1)
            #p1, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'k--')
        else:
            c1 = vertices[i1]
            c2 = vertices[i2]
            p, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'k-')


main()