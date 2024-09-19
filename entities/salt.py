from constants.events import EVENT_NAMES
from entities.entity_base import EntityBase


class Salt(EntityBase):
    def __init__(self):
        super().__init__()

        self.id = "salt"
        # TODO: Insert Salt model when done.
        # self.model = ""

        self.accept(EVENT_NAMES.SNEAKING, self.bad_salt)

    def bad_salt(self, sneak):
        if sneak:
            print("Bad salt")
        elif not sneak:
            print("Good salt!")
