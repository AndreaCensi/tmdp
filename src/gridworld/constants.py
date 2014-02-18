
class GridWorldsConstants:
    Empty = 0
    Obstacle = 1
    action_to_displ = {
       'r': (-1, 0),
       'l': (+1, 0),
       'd': (0, -1),
       'u': (0, +1),
       'rd': (-1, -1),
       'ld': (+1, -1),
       'ru': (-1, +1),
       'lu': (+1, +1),
    }
