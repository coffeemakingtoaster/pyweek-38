from direct.actor.Actor import Actor
from entities.entity_base import EntityBase


class Player(EntityBase):
    def __init__(self):
        super().__init__()

        self.model = Actor("assets/models/PlayerStandin.bam", {"Idle": "assets/models/PlayerStandin.bam"})
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(self.render)


        # Keybinds for movement
        self.accept("a",self.set_movement_status, ["left"])
        self.accept("a-up", self.unset_movement_status, ["left"])
        self.accept("d",self.set_movement_status, ["right"])
        self.accept("d-up", self.unset_movement_status, ["right"])
        self.accept("w",self.set_movement_status, ["up"])
        self.accept("w-up", self.unset_movement_status, ["up"])
        self.accept("s",self.set_movement_status, ["down"])
        self.accept("s-up", self.unset_movement_status, ["down"])

        self.accept("e",self.set_interact)
        # self.accept("e-up", self.unset_interact)
        
        
        self.id = "player"

        def set_movement_status(self, direction):
            self.movement_status[direction] = 1

        def unset_movement_status(self, direction):
            self.movement_status[direction] = 0
        
        def set_interact(self):
            print("Interacting.")
        
        
        def update(self, dt): 
            self.model.node().resetAllPrevTransform()
            