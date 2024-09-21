from constants.events import EVENT_NAMES
from constants.map import TARGETS
import copy

from helpers.dish_helper import VIABLE_FINISHED_ORDER_DISHES
from helpers.pathfinding_helper import get_path_from_to_tile, get_path_from_to_tile_type, global_pos_to_grid, pos_to_string
class Step:
    name = None 
    overwrite_step = None
    next = None
    target = None
    remember_target = None
    target_from_step = None
    release_target_after = None
    repeats=1
    def __init__(self,name,next,target,overwrite_step=None, onfail_goto_step=0, remember_target=False, target_from=None, release_target_after=None, repeats=1) -> None:
        self.name = name
        self.next = next
        self.target = target
        self.overwrite_step = overwrite_step
        self.onfail_goto_step = onfail_goto_step
        self.remember_target = remember_target
        self.target_from_step = target_from 
        self.repeats = repeats
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
        self.previous = None
    
    def get_new_recipe(self, key):
        for state_key in self.state:
            cord_status = base.usage_handler.get_cord_status(self.state[state_key][1])
            if cord_status.status:
                base.usage_handler.set_cord_status(self.state[state_key][1], False, None)
        self.current_step = copy.deepcopy(RECIPES[key])
        messenger.send(EVENT_NAMES.ADD_ORDER, [key])
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
        self.previous = self.current_step
        self.current_step = self.current_step.next

    def recover(self):
        if self.previous is not None:
            # This in addition to is_recovering on the enemy will walk to 0,0 without trying to interact with anything
            self.current_step = self.previous
        else:
            next = self.current_step
            self.current_step = Step(
                "tmp",
                target=None,
                next=next
            )


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
    VIABLE_FINISHED_ORDER_DISHES.SALAD: Step(
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
                                                target=TARGETS.DROPOFF,
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
    VIABLE_FINISHED_ORDER_DISHES.ICE_CREAM: Step(
        "Get chocolate",
        target=TARGETS.CHOCOLATE_STATION,
        next=Step(
            "Cut chocolate",
            target=TARGETS.CUTTING_BOARD,
            remember_target=True,
            next=Step(
                    "Pickup chocolate",
                    target=TARGETS.CUTTING_BOARD,
                    target_from="Cut chocolate",
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
                                        repeats=100,
                                        next=Step(
                                            "Dropoff icecream",
                                            target=TARGETS.DROPOFF,
                                            next=None
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        ),
    VIABLE_FINISHED_ORDER_DISHES.SOUP: Step(
            "Get potato",
            target=TARGETS.POTATO_STATION,
            next=Step(
                "Cut potato",
                target=TARGETS.CUTTING_BOARD,
                remember_target=True,
                next=Step(
                    "Pickup potato",
                    target_from="Cut potato",
                    target=TARGETS.CUTTING_BOARD,
                    next=Step(
                        "Add potato to pot",
                        target=TARGETS.POT,
                        remember_target=True,
                        next=Step(
                            "Get onion",
                            target=TARGETS.ONION_STATION,
                            remember_target=True,
                            next=Step(
                                "Cut onion",
                                remember_target=True,
                                target=TARGETS.CUTTING_BOARD,
                                next=Step(
                                    "Pickup onion",
                                    target=TARGETS.CUTTING_BOARD,
                                    target_from="Cut onion",
                                    next=Step(
                                        "Add onion to pot",
                                        target=TARGETS.POT,
                                        target_from="Add potato to pot",
                                        release_target_after=False,
                                        next=Step(
                                            "Get plate",
                                            target=TARGETS.WASHER,
                                            onfail_goto_step=-1,
                                            next=Step(
                                                "Pickup soup",
                                                target=TARGETS.POT,
                                                target_from="Add potato to pot",
                                                repeats=30,
                                                next=Step(
                                                    "Dropoff",
                                                    target=TARGETS.DROPOFF,
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
        )
    ),
    VIABLE_FINISHED_ORDER_DISHES.STEAK: Step(
        "Get steak",
        target=TARGETS.STEAK_STATION,
        next=Step(
            "Add steak to pan",
            target=TARGETS.PAN,
            remember_target=True,
            next=Step(
                "Get plate",
                target=TARGETS.WASHER,
                onfail_goto_step=-1,
                next=Step(
                    "Get steak from pan",
                    target=TARGETS.PAN,
                    target_from="Add steak to pan",
                    repeats=30,
                    next=Step(
                        "Put plate on countertop",
                        target=TARGETS.COUNTERTOP,
                        remember_target=True,
                        next=Step(
                            "Get potato",
                            target=TARGETS.POTATO_STATION,
                            next=Step(
                                "Cut potato",
                                target=TARGETS.CUTTING_BOARD,
                                remember_target=True,
                                next=Step(
                                    "Pickup potato",
                                    target=TARGETS.CUTTING_BOARD,
                                    target_from="Cut potato",
                                    next=Step(
                                        "Add to fry",
                                        target=TARGETS.FRY,
                                        remember_target=True,
                                        next=Step(
                                            "Get plate",
                                            target_from="Put plate on countertop",
                                            target=TARGETS.COUNTERTOP,
                                            next=Step(
                                                "Get fries",
                                                target=TARGETS.FRY,
                                                target_from="Add to fry",
                                                repeats=30,
                                                next=Step(
                                                    "Dropoff",
                                                    target=TARGETS.DROPOFF,
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
            )
        )
    ),
    VIABLE_FINISHED_ORDER_DISHES.PIZZA: Step(
            "Get plate",
            target=TARGETS.WASHER,
            next=Step(
                "Put plate on countertop",
                target=TARGETS.COUNTERTOP,
                remember_target=True,
                next=Step("Get dough",
                    target=TARGETS.DOUGH_STATION,
                    next=Step(
                        "Put dough on plate",
                        target=TARGETS.COUNTERTOP,
                        target_from="Put plate on countertop",
                        release_target_after=False,
                        next=Step(
                            "Get tomato",
                            target=TARGETS.TOMATO_STATION,
                            next=Step(
                                "Cut tomato",
                                target=TARGETS.CUTTING_BOARD,
                                remember_target=True,
                                next=Step(
                                    "Get my plate",
                                    target=TARGETS.COUNTERTOP,
                                    target_from="Put plate on countertop",
                                    next=Step(
                                        "Get tomato",
                                        target=TARGETS.CUTTING_BOARD,
                                        target_from="Cut tomato",
                                        next=Step(
                                            "Put plate on countertop",
                                            target=TARGETS.COUNTERTOP,
                                            remember_target=True,
                                            next=Step(
                                                "Get cheese",
                                                target=TARGETS.CHEESE_STATION,
                                                next=Step(
                                                    "Cut cheese",
                                                    target=TARGETS.CUTTING_BOARD,
                                                    remember_target=True,
                                                    next=Step(
                                                        "Get my plate",
                                                        target=TARGETS.COUNTERTOP,
                                                        target_from="Put plate on countertop",
                                                        next=Step(
                                                            "Get cheese",
                                                            target=TARGETS.CUTTING_BOARD,
                                                            target_from="Cut cheese",
                                                            next=Step(
                                                                "Put in oven",
                                                                target=TARGETS.OVEN,
                                                                remember_target=True,
                                                                next=Step(
                                                                    "Get from oven",
                                                                    target_from="Put in oven",
                                                                    target=TARGETS.OVEN,
                                                                    repeats=30,
                                                                    next=Step(
                                                                        "Dropoff",
                                                                        target=TARGETS.DROPOFF,
                                                                        next=None,
                                                                )
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
}
