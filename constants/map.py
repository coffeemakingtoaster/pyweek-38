from collections import defaultdict

# TODO: Adapt this
PATHFINDING_MAP = [
    ["#","#","#","#","#","#","#"],
    ["#","C"," "," "," ","A","#"],
    ["#","#","#","#"," "," ","#"],
    ["#","B"," "," ","#"," ","#"],
    ["#"," ","#"," ","#"," ","#"],
    ["#"," ","#"," ","#"," ","#"],
    ["#","C"," ","A"," "," ","#"],
    ["#","#","#","#","#","#","#"],
]

# Build target map
# This could be slow at startup but faster when actually running
TARGET_MAP = defaultdict(lambda: [])
for i in range(len(PATHFINDING_MAP)):
    for j in range(len(PATHFINDING_MAP[i])):
        if PATHFINDING_MAP[i][j] in ['A', 'B', 'C']:
            TARGET_MAP[PATHFINDING_MAP[i][j]].append((i,j))
