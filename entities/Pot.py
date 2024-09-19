from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.item_base import ItemBase
from entities.dish import Dish
from entities.ingredient import Ingredient
from helpers.model_helpers import load_model

class Pot(Station):
    def __init__(self,actor):
        self.id = "IceMaker"
        self.duration = 10
        
        self.inventory = []
        
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if item.id == "chopped_potatoes" or item.id == "chopped_onion":
            if item.id not in self.inventory:
                print("Yay" + item.id)
                self.inventory.append(item.id)
                player.set_holding(ItemBase("empty_hands",load_model("empty_hands")))
            if len(self.inventory) == 2:
                #self.play_anim("Close")
                self.task = taskMgr.do_method_later(self.duration,self.finish_soup,"task")
        elif item.id == "empty_plate" and self.inventory == "unplated_soup":
            player.set_holding(Ingredient("unplated_soup",None))
            self.inventory = []
            
        else:
            #Error Sound
            print("I only eat pizza :()")
            
    def finish_soup(self,name):
        self.inventory = "unplated_soup"
        #self.play_anim("Open")