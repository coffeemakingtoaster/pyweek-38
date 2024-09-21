from queue import PriorityQueue
from constants.enemy_const import MOVEMENT
from constants.map import MAP_COORD_BOUNDS_X, MAP_COORD_BOUNDS_Y, MAP_DIMENSIONS, TARGET_MAP, PATHFINDING_MAP
import datetime

from panda3d.core import Point3

class VisitedNode:
    def __init__(self,score,dist_to_target, pos) -> None:
        self.score = score
        self.rating = score + dist_to_target
        self.pos = pos

# this is n squared and therefore slow as shit!
# For now this is fine as we are working with dummy data
# However in the final version it would probably be best to build a list of target positions once and just reuse it
def __find_closest_target_dist(pos, target, enemy_id):
    dist = 100000
    for target_pos in TARGET_MAP[target]:
        # is currently used?
        cord_status = base.usage_handler.get_cord_status(target_pos)
        if cord_status.status and cord_status.owner != enemy_id:
            continue
        dist = min((pos[0] - target_pos[0])**2 + (pos[1] - target_pos[1])**2, dist)
    return dist

def __optimize_waypoints(waypoints):
    if len(waypoints) < 3:
        return waypoints
    optimized = []
    diff = (0,0)
    for i in range(1,len(waypoints) - 1):
        d = (waypoints[i][0] - waypoints[i-1][0],waypoints[i][1] - waypoints[i-1][1])
        if (d[0] == diff[0] and d[1] == diff[1]) or (d[0] == 0 and d[1] == 0):
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
    # this should never happen
    if 0<pos[0]>len(PATHFINDING_MAP) or 0<pos[0]>len(PATHFINDING_MAP[0]):
        return True
    return PATHFINDING_MAP[pos[0]][pos[1]] == "#"

def pos_to_string(pos):
    return f"{pos[0]}{pos[1]}"

def __backtrack(target_pos, start_pos, visited, debug_print):

    backtrack_pos = target_pos
    waypoints = []

    count = 0

    while True:
        # This should in theory never happen...however better be safe than sorry
        if count > 100:
            return __optimize_waypoints(waypoints + [target_pos])
        waypoints.insert(0,backtrack_pos)
        if backtrack_pos == start_pos:
            break
        min_val = visited[pos_to_string(backtrack_pos)].score
        for pos in __get_adjacent(backtrack_pos):
            if pos_to_string(pos) not in visited:
                continue
            node = visited[pos_to_string(pos)]
            if node is None:
                continue
            if min_val > node.score:
                backtrack_pos = pos
                min_val = node.score
        count += 1

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
            print(PATHFINDING_MAP[i][j][0],end="")
        print()
    return __optimize_waypoints(waypoints)

def get_path_from_to_tile(start_pos, target_pos, debug_print=False):
   
    # if out of bounds -> try and correct rounding errors/try to walk back into bounds
    if not (0 <= start_pos[0] < len(PATHFINDING_MAP)) or not (0 <= start_pos[1] < len(PATHFINDING_MAP[0])):
        start_pos = (
            max(min(start_pos[0],len(PATHFINDING_MAP) - 1),0),
            max(min(start_pos[1],len(PATHFINDING_MAP[0]) - 1),0)
        )

    if PATHFINDING_MAP[start_pos[0]][start_pos[1]] == "#":
        print("\033[91m start in wall?\033[00m")
        
    start_time = datetime.datetime.now()
    todo_queue = PriorityQueue()
    todo_queue.put((1,start_pos))
    visited = dict()
    visited[pos_to_string(start_pos)] = VisitedNode(0,0, start_pos)

    found = False

    # build value grid
    while not todo_queue.empty():
        current = todo_queue.get()[1]

        current_node = visited[pos_to_string(current)]

        if (current[0],current[1]) == target_pos:
            found = True
            break
        
        for adj in __get_adjacent(current):
            if pos_to_string(adj) in visited:
                continue
            adj_visited = VisitedNode(
                current_node.score + 1,
                (adj[0] - target_pos[0])**2 + (adj[1] - target_pos[1])**2,
                adj
            )
            visited[pos_to_string(adj)] = adj_visited
            todo_queue.put((adj_visited.rating, adj))
   
    if not found:
        print("i gotchu homie")
        nodes = [visited[id] for id in visited.keys()]
        nodes.sort(key=lambda node: node.rating)
        target_pos = nodes[0].pos

    res = __backtrack(target_pos, start_pos, visited, debug_print)
    diff = (datetime.datetime.now() - start_time)
    if debug_print:
        print(f"Pathfinding ran for: {diff.total_seconds() * 1000} ms")
    return res

def get_path_from_to_tile_type(start_pos, target, enemy_id=None, debug_print=False):
   
    # if out of bounds -> try and correct rounding errors/try to walk back into bounds
    if not (0 <= start_pos[0] < len(PATHFINDING_MAP)) or not (0 <= start_pos[1] < len(PATHFINDING_MAP[0])):
        start_pos = (
            max(min(start_pos[0],len(PATHFINDING_MAP) - 1),0),
            max(min(start_pos[1],len(PATHFINDING_MAP[0]) - 1),0)
        )

    if PATHFINDING_MAP[start_pos[0]][start_pos[1]] == "#":
        print("\033[91m interrupt!\033[00m")
        
    start_time = datetime.datetime.now()
    todo_queue = PriorityQueue()
    todo_queue.put((1,start_pos))
    visited = dict()
    visited[pos_to_string(start_pos)] = VisitedNode(0,0, start_pos)

    target_pos = None

    # build value grid
    while not todo_queue.empty():
        current = todo_queue.get()[1]

        current_node = visited.get(pos_to_string(current))

        if PATHFINDING_MAP[current[0]][current[1]] == target:
            target_pos = current
            break
        
        for adj in __get_adjacent(current):
            if pos_to_string(adj) in visited:
                continue
            adj_visited = VisitedNode(
                current_node.score + 1,
                __find_closest_target_dist(adj, target, enemy_id),
                adj
            )
            visited[pos_to_string(adj)] = adj_visited
            todo_queue.put((adj_visited.rating, adj))
  
    if target_pos is None:

        print("Could not find target....")
        # this is a recovery strategy! ideally this should never occur
        return [(1,1)]
    
    res = __backtrack(target_pos, start_pos, visited, debug_print)
    diff = (datetime.datetime.now() - start_time)
    if debug_print:
        print(f"Pathfinding ran for: {diff.total_seconds() * 1000} ms")
    return res

def grid_pos_to_global(gridpos):
    return Point3(
        gridpos[1] * (abs(MAP_COORD_BOUNDS_X[0] - MAP_COORD_BOUNDS_X[1])/ MAP_DIMENSIONS[1]) + MAP_COORD_BOUNDS_X[0],
        # this is needed as the transition direction for the y axis is flipped.
        # while the x axis goes from negative to positive, this is the other way round
        -gridpos[0] * (abs(MAP_COORD_BOUNDS_Y[0] - MAP_COORD_BOUNDS_Y[1])/ MAP_DIMENSIONS[0]) + MAP_COORD_BOUNDS_Y[0],
        MOVEMENT.ENEMY_FIXED_HEIGHT
    )

def global_pos_to_grid(global_pos):
    return (
        abs(int(round((global_pos.y - MAP_COORD_BOUNDS_Y[0]) * (MAP_DIMENSIONS[0]/abs(MAP_COORD_BOUNDS_Y[0] - MAP_COORD_BOUNDS_Y[1]))))),
        abs(int(((global_pos.x - MAP_COORD_BOUNDS_X[0]) * (MAP_DIMENSIONS[1]/abs(MAP_COORD_BOUNDS_X[0] - MAP_COORD_BOUNDS_X[1])))))
    )
