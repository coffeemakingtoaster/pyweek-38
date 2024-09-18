from queue import PriorityQueue
from constants.map import MAP_COORD_BOUNDS_X, MAP_COORD_BOUNDS_Y, MAP_DIMENSIONS, TARGET_MAP, PATHFINDING_MAP
import datetime

from panda3d.core import Point3

class VisitedNode:
    def __init__(self,score,dist_to_target) -> None:
        self.score = score
        self.rating = score + dist_to_target

# this is n squared and therefore slow as shit!
# For now this is fine as we are working with dummy data
# However in the final version it would probably be best to build a list of target positions once and just reuse it
def __find_closest_target_dist(pos, target):
    dist = 100000
    for target_pos in TARGET_MAP[target]:
        dist = min((pos[0] - target_pos[0])**2 + (pos[1] - target_pos[1])**2, dist)
    return dist

def __optimize_waypoints(waypoints):
    if len(waypoints) < 3:
        return waypoints
    optimized = []
    diff = (0,0)
    for i in range(1,len(waypoints) - 1):
        d = (waypoints[i][0] - waypoints[i-1][0],waypoints[i][1] - waypoints[i-1][1])
        if d[0] == diff[0] and d[1] == diff[1] or waypoints[i] == waypoints[i-1]:
            continue
        diff = d
        optimized.append(waypoints[i - 1])
    optimized.append(waypoints[-1])
    return optimized

def __get_adjacent(pos):
    res = []

    #x
    if pos[0] > 0:
        if not __is_wall((pos[0]-1, pos[1])):
            res.append((pos[0]-1, pos[1]))

    if pos[0] < MAP_DIMENSIONS[0] - 1:
        if not __is_wall((pos[0]+1, pos[1])):
            res.append((pos[0]+1, pos[1]))

    #y
    if pos[1] > 0:
        if not __is_wall((pos[0], pos[1]-1)):
            res.append((pos[0], pos[1]-1))

    if pos[1] < MAP_DIMENSIONS[1] - 1:
        if not __is_wall((pos[0], pos[1] + 1)):
            res.append((pos[0], pos[1] + 1))

    return res

def __is_wall(pos):
    return PATHFINDING_MAP[pos[0]][pos[1]] == "#"

def __pos_to_string(pos):
    return f"{pos[0]}{pos[1]}"

def get_path_from_to_tile_type(start_pos, target, debug_print=False):
    
    # if out of bounds -> try and correct rounding errors/try to walk back into bounds
    if not (0 <= start_pos[0] < len(PATHFINDING_MAP)) or not (0 <= start_pos[1] < len(PATHFINDING_MAP[0])):
        start_pos = (
            max(min(start_pos[0],len(PATHFINDING_MAP) - 1),0),
            max(min(start_pos[1],len(PATHFINDING_MAP[0]) - 1),0)
        )
        
    start_time = datetime.datetime.now()
    todo_queue = PriorityQueue()
    todo_queue.put((1,start_pos))
    visited = dict()
    visited[__pos_to_string(start_pos)] = VisitedNode(0,0)

    target_pos = None
  
    # build value grid
    while not todo_queue.empty():
        current = todo_queue.get()[1]

        current_node = visited.get(__pos_to_string(current))

        if PATHFINDING_MAP[current[0]][current[1]] == target:
            target_pos = current
            break
        
        for adj in __get_adjacent(current):
            if __pos_to_string(adj) in visited:
                continue
            adj_visited = VisitedNode(
                current_node.score + 1,
                __find_closest_target_dist(adj, target)
            )
            visited[__pos_to_string(adj)] = adj_visited
            todo_queue.put((adj_visited.rating, adj))
   
    if target_pos is None:

        print("Could not find target....")
        return []

    backtrack_pos = target_pos

    waypoints = []

    count = 0

    while True:
        # This should in theory never happen...however better be safe than sorry
        if count > 1000:
            return waypoints + [target_pos]
        waypoints.append(backtrack_pos)
        if backtrack_pos == start_pos:
            break
        min_val = visited[__pos_to_string(backtrack_pos)].score
        for pos in __get_adjacent(backtrack_pos):
            if __pos_to_string(pos) not in visited:
                continue
            node = visited[__pos_to_string(pos)]
            if node is None:
                continue
            if min_val > node.score:
                backtrack_pos = pos
                min_val = node.score
        count += 1

    diff = (datetime.datetime.now() - start_time)
    print(f"Pathfinding ran for: {diff.total_seconds() * 1000} ms")

    waypoints = list(set(waypoints))

    if not debug_print:
        return __optimize_waypoints(waypoints)

    # Backtrack
    map_overlay = []
    for i in range(len(PATHFINDING_MAP)):
        map_overlay.append([None] * len(PATHFINDING_MAP[0]))

    for wp in waypoints:
        map_overlay[wp[0]][wp[1]] = "\033[96m.\033[00m"

    map_overlay[target_pos[0]][target_pos[1]] = "\033[95mT\033[00m"

    map_overlay[backtrack_pos[0]][backtrack_pos[1]] = "\033[93mS\033[00m"

    for i in range(len(PATHFINDING_MAP)):
        for j in range(len(PATHFINDING_MAP[i])):
            if map_overlay[i][j] is not None:
                print(map_overlay[i][j],end="")
                continue
            print(PATHFINDING_MAP[i][j],end="")
        print()
    print(__optimize_waypoints(waypoints)
)
    return __optimize_waypoints(waypoints)

def grid_pos_to_global(gridpos):
    return Point3(
        gridpos[1] * (abs(MAP_COORD_BOUNDS_X[0] - MAP_COORD_BOUNDS_X[1])/ MAP_DIMENSIONS[1]) + MAP_COORD_BOUNDS_X[0],
        # this is needed as the transition direction for the y axis is flipped.
        # while the x axis goes from negative to positive, this is the other way round
        -gridpos[0] * (abs(MAP_COORD_BOUNDS_Y[0] - MAP_COORD_BOUNDS_Y[1])/ MAP_DIMENSIONS[0]) + MAP_COORD_BOUNDS_Y[0],
        0
    )

def global_pos_to_grid(global_pos):

    return (
        abs(int(round((global_pos.y - MAP_COORD_BOUNDS_Y[0]) * (MAP_DIMENSIONS[0]/abs(MAP_COORD_BOUNDS_Y[0] - MAP_COORD_BOUNDS_Y[1]))))),
        abs(int(((global_pos.x - MAP_COORD_BOUNDS_X[0]) * (MAP_DIMENSIONS[1]/abs(MAP_COORD_BOUNDS_X[0] - MAP_COORD_BOUNDS_X[1])))))
    )
