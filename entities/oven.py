from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.item_base import ItemBase
from entities.dish import Dish
from helpers.model_helpers import load_model

class Oven(Station):
    def __init__(self,actor):
        self.id = "Oven"
        self.duration = 10
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if item.id == "raw_pizza":
            print("Yay Pizza")
            self.inventory = Dish(item.id,load_model(item.id))
            self.play_anim("Open")
            self.play_anim("Close")
            
        else:
            #Error Sound
            print("I only eat pizza :()")
            
            


