from entities.station import Station


class FreezerDoor(Station):
    def __init__(self, actor):
        self.name = "freezer_door"
        super().__init__(self.name, actor)

        self.open = False

    def interact(self, item, player):
        player_position = player.model.getX()
        if player.id == "player":
            if self.open:
                self.model.play("Close")
                self.open = False
            elif not self.open:
                self.model.play("Open")
                self.open = True
        elif not player.id == "player":
            if self.open:
                self.model.play("Close")
                self.open = False
            elif not self.open and player_position < 3.5:
                self.model.play("Open")
                self.open = True
