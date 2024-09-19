from collections import defaultdict

from panda3d.core import Point3, LVector3

# TODO: Adapt this

MAP_DIMENSIONS = (16,28)

MAP_COORD_BOUNDS_X = (-5.5,6)
MAP_COORD_BOUNDS_Y = (1.5,-5.2)

PATHFINDING_MAP = [
["#"]*MAP_DIMENSIONS[1],
['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'Potato', 'Potato', 'Tomato', 'Tomato', ' ', '#'],
['#', ' ', ' ', ' ', ' ', ' ', 'Fry', ' ', 'Fry', 'Pot', 'Pan', ' ', 'Cutting', ' ', 'Cutting', ' ', 'Pot', 'Pan', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', 'Cheese', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#'],
['#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', 'Onion', '#'],
['#', '#', 'Oven', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', 'Trash', '#', ' ', ' ', ' ', ' ', ' ', '#'],
['#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', 'Salad', '#'],
['#', '#', 'Oven', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Salad', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Salad', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'Ice', ' ', 'Steak', ' ', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Dough', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', 'Cutting', 'Cutting', ' ', 'Cutting', ' ', 'Washer', ' ', ' ', 'Washer', ' ', ' ', 'Icer', ' ', ' ', ' ', '#', 'Chocolate', ' ', 'Cheese', 'A', '#'],
["#"]*MAP_DIMENSIONS[1],
]

# Build target map
# This could be slow at startup but faster when actually running
TARGET_MAP = defaultdict(lambda: [])
for i in range(len(PATHFINDING_MAP)):
    for j in range(len(PATHFINDING_MAP[i])):
        if PATHFINDING_MAP[i][j] in ['A', 'B']:
            TARGET_MAP[PATHFINDING_MAP[i][j]].append((i,j))

MODEL_COLLISION_DIMENSION_LOOKUP = {
    "Cabinet": LVector3(0.5,0.5,1),
    "Storage_Large_Metal": LVector3(1.2,0.3,1),
    "Countertop": LVector3(0.35,0.36,1),
    "Countertop_Medium": LVector3(0.9,0.36,1),
    "Countertop_Large":  LVector3(1.75,0.36,1),
    "Stove": LVector3(0.51,0.35,1),
    "Storage_Medium": LVector3(0.4,1.1,1),
    "Storage_Large": LVector3(1.3,0.4,1),
}

MODEL_COLLISION_OFFSET_LOOKUP = {
    "Cabinet": Point3(0.5,0.5,0),
    "Storage_Large_Metal": Point3(1.2,0.4,1),
    "Countertop": Point3(0.35,0.35,1),
    "Countertop_Medium": Point3(0.9,0.35,1),
    "Countertop_Large":  Point3(1.75,0.35,1),
    "Stove": Point3(0.42,0.35,1),
    "Storage_Medium": LVector3(0.3,1.1,1),
    "Storage_Large": LVector3(1.3,0.3,1),
}
