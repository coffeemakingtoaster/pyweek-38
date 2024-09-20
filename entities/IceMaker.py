from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from constants.map import TARGETS
from entities.station import Station
from entities.item_base import ItemBase
from entities.dish import Dish
from entities.ingredient import Ingredient
from helpers.model_helpers import load_model

class IceMaker(Station):
    def __init__(self,actor):
        self.id = TARGETS.ICEMAKER
        self.duration = 10
        
        self.inventory = []
        
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if (item.id == "ice_cubes" or item.id == "chopped_chocolate")and self.inventory is not "unplated_ice_cream" and len(self.inventory) is not 2:
            if item.id not in self.inventory:
                print("Yay" + item.id)
                self.inventory.append(item.id)
                player.set_holding(ItemBase("empty_hands",load_model("empty_hands")))
            if len(self.inventory) == 2:
                self.play_anim("Close")
                self.task = taskMgr.do_method_later(self.duration,self.finish_ice,"task")
        elif item.id == "empty_plate" and self.inventory == "unplated_ice_cream":
            player.set_holding(Ingredient("unplated_ice_cream",None))
            self.inventory = []
            
        else:
            #Error Sound
            print("I only eat pizza :()")
            
    def finish_ice(self,name):
        self.inventory = "unplated_ice_cream"
        self.play_anim("Open")
        self.task = None
                
