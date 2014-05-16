from gridmaps.map import GridMap
from gridmaps.raytracing import lineofsight

def gridmap_test_occluded():
    W = GridMap.W
    E = GridMap.E
    blocks = [
        [W, W, W],
        [W, E, E],
        [W, W, W],
    ]
    gm = GridMap(blocks=blocks)

    c = [1, 1]
    assert lineofsight(gm, c, [0, 0])
    assert lineofsight(gm, c, [1, 0])
    assert lineofsight(gm, c, [2, 0])
    assert lineofsight(gm, c, [0, 1])
    assert lineofsight(gm, c, [2, 1])
    assert lineofsight(gm, c, [1, 2])
    assert lineofsight(gm, c, [2, 2])


    assert lineofsight(gm, c, [0, 2])
