
from gridmaps.map import GridMap

W = GridMap.W
E = GridMap.E
I = GridMap.I
G = GridMap.G
S = GridMap.S

def map_intruder_1():
    blocks =[
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, I, I, I, W, W, W, W, W, W, I, I, I, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, E, E, S, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)



def map_intruder_3():
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, I, I, I, E, E, E, E, E, W],
        [W, E, E, W, W, W, W, W, W, W, W, W, E, W],
        [W, E, E, E, E, E, S, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)


def map_intruder_2():
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, E, E, E, I, W, I, E, E, E, E, W],
        [W, E, W, E, E, E, I, W, I, E, E, W, E, W],
        [W, E, W, E, E, E, I, W, I, E, E, W, E, W],
        [W, E, W, E, E, E, I, W, I, E, E, W, E, W],
        [W, E, E, E, E, E, I, W, I, E, E, W, E, W],
        [W, E, W, E, E, E, I, W, I, I, I, W, E, W],
        [W, E, W, E, E, E, I, W, W, W, W, W, E, W],
        [W, E, W, I, I, I, I, W, W, W, W, W, E, W],
        [W, E, W, W, W, W, W, W, W, W, W, W, E, W],
        [W, E, E, E, E, E, S, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)



def map_intruder_4():
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, E, E, E, W, I, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, E, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, E, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, I, W, E, W],
        [W, E, W, E, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, I, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, W, W, W, W, W, W, W, W, W, E, W],
        [W, E, E, E, S, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)


def map_intruder_5():
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, E, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, E, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, I, W, E, E, E, E, W, W, W, W, W, I, W],
        [W, E, W, E, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, W, W, W, W, W, W, W, W, W, E, W],
        [W, W, E, E, S, E, E, E, E, E, E, E, W, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)
    
def map_intruder_6():
    """ This has 3 distinct rooms, 2 intruders each. """
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, E, E, E, W, I, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, I, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, W, W, W, W, W, E, E, E, W, E, W],
        [W, E, W, I, E, E, E, W, E, E, I, W, E, W],
        [W, E, W, E, E, E, E, W, W, W, W, W, E, W],
        [W, E, E, E, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, E, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, I, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, W, W, W, W, W, W, W, W, W, E, W],
        [W, E, E, E, S, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)


def map_tmaze():
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, G, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, W, W, W, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, S, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ]
    return GridMap(blocks=blocks)

def map_rmaze():
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, S, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, E, W],
        [W, E, E, E, W, W, W, W, W, W, E, E, G, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ]
    return GridMap(blocks=blocks)

