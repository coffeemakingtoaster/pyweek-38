from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.dish import Dish

class Plate_Station(Station):
    def __init__(self,actor):
        self.id = "Plate_Station"
         
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if item.id == "empty_hands" and inventory[0] is not None:
            player.setHolding(inventory[0])
            return True
        return False
