from collections import defaultdict

# TODO: Adapt this

MAP_DIMENSIONS = (8,14)

MAP_COORD_BOUNDS_X = (-5,6)
MAP_COORD_BOUNDS_Y = (1,-5.2)

PATHFINDING_MAP = [
    ["#"]*MAP_DIMENSIONS[1],
    ["#","B"," "," "," "," "," "," "," "," ","#"," "," ","#"],
    ["#"," "," "," ","#","#","#","#","#"," ","#"," "," ","#"],
    ["#"," "," "," ","#"," "," "," "," "," "," "," "," ","#"],
    ["#"," "," "," ","#"," "," "," "," "," ","#","#","#","#"],
    ["#"," "," "," ","#","#","#","#"," "," "," "," ","A","#"],
    ["#"," "," "," "," "," "," "," "," "," ","#"," "," ","#"],
    ["#"]*MAP_DIMENSIONS[1],
]

# Build target map
# This could be slow at startup but faster when actually running
TARGET_MAP = defaultdict(lambda: [])
for i in range(len(PATHFINDING_MAP)):
    for j in range(len(PATHFINDING_MAP[i])):
        if PATHFINDING_MAP[i][j] in ['A', 'B']:
            TARGET_MAP[PATHFINDING_MAP[i][j]].append((i,j))
