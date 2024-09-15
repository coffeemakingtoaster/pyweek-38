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
