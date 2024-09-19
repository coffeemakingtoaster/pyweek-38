from constants.map import TARGETS
import copy

class Step:
    name = None 
    overwrite_step = None
    next = None
    target = None
    def __init__(self,name,next,target,overwrite_step=None, onfail_goto_step=0) -> None:
        self.name = name
        self.next = next
        self.target = target
        self.overwrite_step = overwrite_step
        self.onfail_goto_step = onfail_goto_step

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

def build_overwrite_routine(current: Step,key="example"):
    print("\033[91m interrupt!\033[00m")
    routine = copy.deepcopy(FALLBACK_ROUTINE[key])
    start_step = routine 
    c = start_step
    while c.next is not None:
        print(c.name)
        c = c.next
    c.next = current
    return start_step

RECIPES = {
    "salad": Step(
            "Get salad",
            target=TARGETS.SALAD_STATION,
            next=Step(
                "Cut salad",
                target=TARGETS.CUTTING_BOARD,
                next=Step(
                    "Get plate",
                    target=TARGETS.WASHER,
                    onfail_goto_step=2,
                    next=Step(
                        "Get the chopped salad",
                        # TODO: add the ability for the behaviour to set ids and try to reach them
                        target=TARGETS.CUTTING_BOARD,
                        next=Step(
                            "Drop off plate with salad",
                            target=TARGETS.COUNTERTOP,
                            next=Step(
                                "Get tomato",
                                target=TARGETS.TOMATO_STATION,
                                next=Step(
                                    "Cut tomato",
                                    target=TARGETS.CUTTING_BOARD,
                                    next=Step(
                                        "Get plate with salad",
                                        #TODO: do with id
                                        target=TARGETS.COUNTERTOP,
                                        next=Step(
                                            "Retrieve the chopped tomato",
                                            onfail_goto_step=5,
                                            target=TARGETS.CUTTING_BOARD,
                                            next=Step(
                                                "Dropoff",
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
            #TODO: implement that a failstep of -1 means: goto trash and get a new recipe
            onfail_goto_step=-1,
            next=Step(
                "Get ice",
                target=TARGETS.ICE_STATION,
                next=Step(
                    "Add ice to icecreammachine",
                    target=TARGETS.ICEMAKER,
                    next=Step(
                        "Get Plate",
                        target=TARGETS.WASHER,
                        onfail_goto_step=-1,
                        next=Step(
                            "Get icecream",
                            target=TARGETS.ICEMAKER,
                            next=Step(
                                "Dropoff icecream",
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
