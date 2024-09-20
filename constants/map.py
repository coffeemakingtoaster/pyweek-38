from collections import defaultdict

from panda3d.core import Point3, LVector3

# TODO: Adapt this

MAP_DIMENSIONS = (16,28)

MAP_COORD_BOUNDS_X = (-5.5,6)
MAP_COORD_BOUNDS_Y = (1.5,-5.2)

class TARGETS:
    OVEN = "Oven"
    FRY = "Fry"
    POT = "Pot"
    PAN = "Pan"
    CUTTING_BOARD = "Cutting Board"
    TRASH = "Trash"
    WASHER = "Washer"
    ICEMAKER = "Icemaker"
    POTATO_STATION = "Potato Station"
    TOMATO_STATION = "Tomato Station"
    CHEESE_STATION = "Cheese Station"
    ONION_STATION = "Onion Station"
    ICE_STATION = "Ice Station"
    STEAK_STATION = "Steak Station"
    DOUGH_STATION = "Dough Station"
    CHOCOLATE_STATION = "Chocolate Station"
    SALAD_STATION = "Salad Station"
    COUNTERTOP = "Countertop"
    STORAGE_DOOR = "Storage Door"
    CHILI_STATION = "Chili Station"

TARGET_BLOCKING_MAP = defaultdict(lambda: False,{
    TARGETS.OVEN:  True,
    TARGETS.FRY: True,
    TARGETS.POT: True,
    TARGETS.CUTTING_BOARD: True,
    TARGETS.COUNTERTOP: True,
    TARGETS.ICEMAKER: True,
    TARGETS.PAN: True,
})

PATHFINDING_MAP = [
["#"]*MAP_DIMENSIONS[1],
['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', TARGETS.POTATO_STATION, TARGETS.POTATO_STATION, TARGETS.TOMATO_STATION, TARGETS.TOMATO_STATION, ' ', '#'],
['#', ' ', ' ', ' ', ' ', ' ', TARGETS.FRY, ' ', TARGETS.FRY, TARGETS.POT, TARGETS.PAN, ' ', TARGETS.CUTTING_BOARD, ' ', TARGETS.CUTTING_BOARD, ' ', TARGETS.POT, TARGETS.PAN, ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', TARGETS.CHILI_STATION, '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#'],
['#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', TARGETS.ONION_STATION, '#'],
['#', '#', TARGETS.OVEN, ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', TARGETS.TRASH, '#', ' ', ' ', ' ', ' ', ' ', '#'],
['#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', TARGETS.SALAD_STATION, '#'],
['#', '#', TARGETS.OVEN, ' ', ' ', ' ', ' ', '#', TARGETS.COUNTERTOP, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', TARGETS.SALAD_STATION, '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', TARGETS.COUNTERTOP, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', TARGETS.SALAD_STATION, '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', TARGETS.COUNTERTOP, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', TARGETS.ICE_STATION, ' ', TARGETS.STEAK_STATION, ' ', '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', TARGETS.DOUGH_STATION, '#'],
['#', ' ', ' ', ' ', ' ', ' ', ' ', TARGETS.CUTTING_BOARD, TARGETS.CUTTING_BOARD, ' ', TARGETS.CUTTING_BOARD, ' ', TARGETS.WASHER, ' ', ' ', TARGETS.WASHER, ' ', ' ', TARGETS.ICEMAKER, ' ', ' ', ' ', '#', TARGETS.CHOCOLATE_STATION, ' ', TARGETS.CHEESE_STATION, ' ', '#'],
["#"]*MAP_DIMENSIONS[1],
]

# Build target map
# This could be slow at startup but faster when actually running
TARGET_MAP = defaultdict(lambda: [])
for i in range(len(PATHFINDING_MAP)):
    for j in range(len(PATHFINDING_MAP[i])):
        if PATHFINDING_MAP[i][j] in [" ","#"]:
            continue
        try:
            TARGET_MAP[PATHFINDING_MAP[i][j]].append((i,j))
        except:
            pass

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
