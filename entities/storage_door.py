from entities.station import Station


class StorageDoor(Station):
    def __init__(self, actor):
        self.name = "freezer_door"
        super().__init__(self.name, actor)

        self.open = False

    def interact(self, item, player):
        if self.open:
            self.model.play("Close")
            self.open = False
        elif not self.open:
            self.model.play("Open")
            self.open = True
