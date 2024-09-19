from constants.events import EVENT_NAMES
from entities.entity_base import EntityBase


class Spice(EntityBase):
    def __init__(self):
        super().__init__()

        self.id = "spice"
        # TODO: Insert Spice model when done.
        # self.model = ""

        self.accept(EVENT_NAMES.SNEAKING, self.bad_spice)

    def bad_spice(self, sneak):
        if sneak:
            print("Bad spice")
        elif not sneak:
            print("Good spice!")
