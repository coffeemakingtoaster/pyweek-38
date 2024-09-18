from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.item_base import ItemBase
from entities.dish import Dish
from entities.ingredient import Ingredient
from helpers.model_helpers import load_model

class Fry(Station):
    def __init__(self,actor):
        self.id = "Fry"
        self.duration = 10
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if item.id == "chopped_potatoes":
            print("potatoes!!!")
            #TODO
            self.inventory = Ingredient("fries",load_model("fries"))
            self.play_anim("Fry")
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
        elif (item.id == "empty_hands" or type(item) == Dish) and  self.inventory.id == "fries":
            player.set_holding(Ingredient("fries",load_model("fries")))
        
        
        else:
            #Error Sound
            print("I only eat fries :()")