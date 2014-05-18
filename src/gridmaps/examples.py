
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


def map_intruder_4c():
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, E, E, E, W, E, E, I, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, E, E, W],
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

def map_intruder_4d():
    """ Vede uno prima dell'altro """
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, E, E, E, W, E, E, I, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, E, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, E, E, I, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, I, W, E, W],
        [W, E, W, E, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, E, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, W, W, W, W, W, W, W, W, W, E, W],
        [W, E, E, E, S, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)

def map_intruder_4a():
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, E, E, E, W, I, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, E, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, E, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, I, E, E, E, W, W, W, W, W, E, W],
        [W, E, W, W, W, W, W, W, W, W, W, W, E, W],
        [W, E, E, E, S, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)


def map_intruder_4b():
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
        [W, E, W, E, E, E, E, W, W, W, W, W, E, W],
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
    """ This has 3 distinct rooms. """
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
        [W, E, E, E, E, E, E, W, S, E, E, W, E, W],
        [W, E, W, E, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, I, E, E, E, W, E, E, E, W, E, W],
        [W, E, W, W, W, W, W, W, W, E, W, W, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ]
    return GridMap(blocks=blocks)



def map_intruder_7():
    """ This has 3 distinct rooms, full of intruders each. """
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, E, E, I, W, I, E, E, E, E, W],
        [W, E, E, E, E, E, I, W, I, E, I, W, E, W],
        [W, E, W, I, E, E, I, W, I, E, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, E, I, W, E, W],
        [W, E, W, W, W, W, W, W, I, E, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, E, E, I, W, W, W, W, W, E, W],
        [W, E, E, E, E, E, I, W, W, W, W, W, E, W],
        [W, E, W, I, E, E, I, W, W, W, W, W, E, W],
        [W, E, W, I, I, I, I, W, W, W, W, W, E, W],
        [W, E, W, W, W, W, W, W, W, W, W, W, E, W],
        [W, E, E, E, S, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)

def map_intruder_8():
    """ This has 3 distinct rooms, full of intruders each, start in 4th room. """
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, E, E, I, W, I, E, E, E, E, W],
        [W, E, E, E, E, E, I, W, I, E, I, W, E, W],
        [W, E, W, I, E, E, I, W, I, E, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, E, I, W, E, W],
        [W, E, W, W, W, W, W, W, I, E, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, E, E, I, W, W, W, W, W, E, W],
        [W, E, E, E, E, E, I, W, S, E, E, W, E, W],
        [W, E, W, I, E, E, I, W, E, E, E, W, E, W],
        [W, E, W, I, I, I, I, W, E, E, E, W, E, W],
        [W, E, W, W, W, W, W, W, W, E, W, W, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)


def map_intruder_10():
    """ This has 3 distinct rooms, full of intruders each, start in 4th room. """
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, E, E, W],
        [W, E, E, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, W, W, W, W, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, W, W, W, W, E, W],
        [W, E, E, I, I, I, I, W, S, E, E, W, E, W],
        [W, E, W, I, I, I, I, W, E, E, E, W, E, W],
        [W, E, W, I, I, I, I, W, E, E, E, W, E, W],
        [W, E, W, W, W, W, W, W, W, E, W, W, E, W],
        [W, E, E, E, E, E, E, E, E, E, E, E, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)

def map_intruder_11():
    """ This has 3 distinct rooms, full environment """
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, I, I, W],
        [W, I, I, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, W, W, W, W, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, W, W, W, W, I, W],
        [W, I, I, I, I, I, I, W, E, S, E, W, I, W],
        [W, I, W, I, I, I, I, W, E, E, E, W, I, W],
        [W, I, W, I, I, I, I, W, E, E, E, W, I, W],
        [W, I, W, W, W, W, W, W, W, E, W, W, I, W],
        [W, I, I, I, I, I, I, I, I, E, I, I, I, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)


def map_intruder_12():
    """ This has 2 distinct rooms, full environment """
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, I, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, I, I, I, W, I, W],
        [W, I, W, I, I, I, I, W, W, W, W, W, I, W],
        [W, I, I, I, I, I, I, W, E, S, E, W, I, W],
        [W, I, W, I, I, I, I, W, E, E, E, W, I, W],
        [W, I, W, I, I, I, I, W, E, E, E, W, I, W],
        [W, I, W, W, W, W, W, W, W, E, W, W, I, W],
        [W, I, I, I, I, I, I, I, I, E, I, I, I, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W]
    ]
    return GridMap(blocks=blocks)


def map_intruder_9():
    """ 2 rooms, full of area """
    blocks = [
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, E, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, E, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, I, I, I, I, W, I, I, I, W, E, W],
        [W, E, W, W, W, W, W, W, W, W, W, W, E, W],
        [W, E, E, E, E, E, S, E, E, E, E, E, E, W],
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



# Need to have more than one intruder cell
# def map_test00():
#     blocks = [
#         [W, W, W, W, W],
#         [W, E, E, I, W],
#         [W, E, W, E, W],
#         [W, S, W, E, W],
#         [W, W, W, W, W],
#     ]
#     return GridMap(blocks=blocks)

def map_test01():
    """ 0 bits """
    blocks = [
        [W, W, W, W, W],
        [W, E, E, I, W],
        [W, E, W, E, W],
        [W, S, W, I, W],
        [W, W, W, W, W],
    ]
    return GridMap(blocks=blocks)


def map_test02():
    """ 0 bits """
    blocks = [
        [W, W, W, W, W],
        [W, I, E, E, W],
        [W, E, W, E, W],
        [W, S, W, I, W],
        [W, W, W, W, W],
    ]
    return GridMap(blocks=blocks)


def map_test03():
    """ 1 bits, 2 states, 4 trajectories """
    blocks = [
        [W, W, W, W, W, W, W],
        [W, E, E, S, E, E, W],
        [W, I, W, W, W, I, W],
        [W, I, W, W, W, I, W],
        [W, W, W, W, W, W, W],
    ]
    return GridMap(blocks=blocks)


def map_test04():
    """ 0 bits, 1 state, 3 trajectories """
    blocks = [
        [W, W, W, W, W, W, W],
        [W, E, E, S, E, E, W],
        [W, I, W, W, W, E, W],
        [W, I, W, W, W, I, W],
        [W, W, W, W, W, W, W],
    ]
    return GridMap(blocks=blocks)
