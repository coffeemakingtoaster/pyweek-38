from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.dish import Dish
from entities.ingredient import Ingredient
from entities.item_base import ItemBase
from helpers.model_helpers import load_model

class Trash_Station(Station):
    def __init__(self,actor):
        self.id = "Trash_Station"
        
        self.inventory = [Dish("empty_plate",load_model("empty_plate")),Dish("empty_plate",load_model("empty_plate"))]
        
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if type(item) == Ingredient or item.id == "empty_plate":
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            return True
        return False