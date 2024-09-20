from constants.map import TARGETS
import copy

from helpers.pathfinding_helper import get_path_from_to_tile, get_path_from_to_tile_type, global_pos_to_grid, pos_to_string
class Step:
    name = None 
    overwrite_step = None
    next = None
    target = None
    remember_target = None
    target_from_step = None
    release_target_after = None
    def __init__(self,name,next,target,overwrite_step=None, onfail_goto_step=0, remember_target=False, target_from=None, release_target_after=None) -> None:
        self.name = name
        self.next = next
        self.target = target
        self.overwrite_step = overwrite_step
        self.onfail_goto_step = onfail_goto_step
        self.remember_target = remember_target
        self.target_from_step = target_from 
        if target_from is not None:
            # Assume that after this use the station is not needed by this npc anymore
            if release_target_after is None:

                self.release_target_after = True
            else:
                self.release_target_after = False

class Routine:
    def __init__(self, start_step=None, key=None) -> None:

        self.state = dict()
        if start_step is not None:
            self.current_step = start_step
        else:
            self.get_new_recipe(key)
    
    def get_new_recipe(self, key):
        for state_key in self.state:
            cord_status = base.usage_handler.get_cord_status(self.state[state_key][1])
            if cord_status.status:
                base.usage_handler.set_cord_status(self.state[state_key][1], False, None)
        self.current_step = copy.deepcopy(RECIPES[key])
        self.state = {}

    def get_step_target_uuid(self):
        if self.current_step.target_from_step is not None:
            if self.current_step.target_from_step not in self.state:
                print(self.state)
                print(self.current_step.target_from_step)
                print(self.state[self.current_step.target_from_step])
                print("Warning! Callback to unknown step")
                return None
            return self.state[self.current_step.target_from_step]
        return None

    def update_memory(self, uuid, pos):
        if self.current_step.remember_target:
            print(f"Oh i better remember this {self.current_step.target}")
            self.state[self.current_step.name] = (uuid,pos)

    def advance(self):
        self.current_step = self.current_step.next

    def get_waypoints(self, start_pos, enemy_id):
        # goto any station
        if self.current_step.target_from_step is not None:
            print(self.get_step_target_uuid()[1])
            return get_path_from_to_tile(
                global_pos_to_grid(start_pos),
                self.get_step_target_uuid()[1]
            )
        else:
            return get_path_from_to_tile_type(global_pos_to_grid(start_pos),self.current_step.target, enemy_id) 

    def insert_immediate_overwrite(self, key):
        routine = copy.deepcopy(FALLBACK_ROUTINE[key])
        start_step = routine 
        c = start_step
        while c.next is not None:
            print(c.name)
            c = c.next
        c.next = self.current_step 
        self.current_step = start_step

# untested
def get_routine_at_step(key, step):
    curr = copy.deepcopy(RECIPES[key])
    for i in range(step):
        curr = curr.next
    return curr.next

# This is an example
FALLBACK_ROUTINE = {
    "example": Step(
        "Visit trash",
        target=TARGETS.TRASH,
        next=Step(
            "Visit freezer",
            target=TARGETS.CHOCOLATE_STATION,
            next=None
    ))
}

RECIPES = {
    "salad": Step(
            "Get salad",
            target=TARGETS.SALAD_STATION,
            next=Step(
                "Cut salad",
                target=TARGETS.CUTTING_BOARD,
                remember_target=True,
                next=Step(
                    "Get plate",
                    target=TARGETS.WASHER,
                    onfail_goto_step=2,
                    next=Step(
                        "Get the chopped salad",
                        target=TARGETS.CUTTING_BOARD,
                        target_from="Cut salad",
                        next=Step(
                            "Drop off plate with salad",
                            target=TARGETS.COUNTERTOP,
                            remember_target=True,
                            next=Step(
                                "Get tomato",
                                target=TARGETS.TOMATO_STATION,
                                next=Step(
                                    "Cut tomato",
                                    target=TARGETS.CUTTING_BOARD,
                                    remember_target=True,
                                    next=Step(
                                        "Get plate with salad",
                                        target=TARGETS.COUNTERTOP,
                                        target_from="Drop off plate with salad",
                                        next=Step(
                                            "Retrieve the chopped tomato",
                                            onfail_goto_step=5,
                                            target=TARGETS.CUTTING_BOARD,
                                            target_from="Cut tomato",
                                            next=Step(
                                                "Dropoff",
                                                # TODO: change this to dropoff zone
                                                target=TARGETS.COUNTERTOP,
                                                next=None
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    ),
    "chocolate_icecream": Step(
        "Get chocolate",
        target=TARGETS.CHOCOLATE_STATION,
        next=Step(
            "Put chocolate into icemachine",
            target=TARGETS.ICEMAKER,
            remember_target=True,
            onfail_goto_step=-1,
            next=Step(
                "Get ice",
                target=TARGETS.ICE_STATION,
                next=Step(
                    "Add ice to icecreammachine",
                    target=TARGETS.ICEMAKER,
                    target_from="Put chocolate into icemachine",
                    release_target_after=False,
                    next=Step(
                        "Get Plate",
                        target=TARGETS.WASHER,
                        onfail_goto_step=-1,
                        next=Step(
                            "Get icecream",
                            target=TARGETS.ICEMAKER,
                            target_from="Put chocolate into icemachine",
                            next=Step(
                                "Dropoff icecream",
                                #TODO: change this to dropoff zone
                                target=TARGETS.COUNTERTOP,
                                next=None
                            )
                        )
                    )
                )
            )
        )
    )
}
