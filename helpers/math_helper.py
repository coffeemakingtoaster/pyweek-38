from panda3d.core import CollisionNode, CollisionHandlerQueue, CollisionRay, CollisionEntry

from constants.layers import MAP_COLLISION_BITMASK

def get_limited_rotation_target(current, target, limit):
    # Normalize the angles to be within the range -180 to 180
    def normalize_angle(angle):
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle
    
    # Calculate the difference between the current and target angles
    delta = normalize_angle(target - current)
    
    # Limit the rotation to the specified limit
    if delta > limit:
        delta = limit
    elif delta < -limit:
        delta = -limit
    
    # Calculate the new target angle based on the limited rotation
    new_target = normalize_angle(current + delta)
    
    return new_target

def get_first_intersection(starting_pos, direction) -> CollisionEntry:
    pq = CollisionHandlerQueue()
    picker_np = render.attachNewNode(CollisionNode('dashray'))
    picker_np.node().addSolid(CollisionRay(starting_pos, direction))
    picker_np.node().setCollideMask(MAP_COLLISION_BITMASK)
    #picker_np.show()
    base.cTrav.addCollider(picker_np,pq)
    base.cTrav.traverse(render)
    base.cTrav.removeCollider(picker_np)
    if len(pq.getEntries()) == 0:
        return None
    pq.sort_entries()
    #picker_np.removeNode()
    if pq.getNumEntries() > 0:
        return pq.getEntry(0)
    return None
