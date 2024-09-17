from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.dish import Dish

class Countertop(Station):
    def __init__(self,actor):
        self.id = "Countertop"
         
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if item.id == "empty_hands" and inventory[0] is not None:
            player.holding = inventory[0]
        elif len(inventory) == 0 or inventory[0] is None:
            player.holding = Itembase("empty_hands",None)
            inventory.append(player.holding)
        elif type(item) is Dish:
            item.add_ingredient(item)
            