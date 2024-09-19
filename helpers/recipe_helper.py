from constants.map import TARGETS
import copy


class Step:
    name = None 
    overwrite_step = None
    next = None
    target = None
    def __init__(self,name,next,target,overwrite_step=None) -> None:
        self.name = name
        self.next = next
        self.target = target
        self.overwrite_step = overwrite_step

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
    )
}
