from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.item_base import ItemBase
from entities.dish import Dish
from entities.ingredient import Ingredient
from helpers.model_helpers import load_model

class Pan(Station):
    def __init__(self,actor):
        self.id = "Pan"
        self.duration = 5
        
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if item.id == "raw_steak":
            self.inventory = Ingredient(item.id,load_model(item.id))
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            self.render()
            #self.play_anim("PanFry")
            self.task = taskMgr.doMethodLater(self.duration,self.finish_pan_fry,"task")
            
        elif (item.id == "empty_hands" or type(item) == Dish) and self.inventory.id == "steak":
            player.set_holding(Ingredient("steak",load_model("steak")))
            self.clean()
            self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
            self.render()
        
        else:
            #Error Sound
            print("I only eat steak:()")
            
            
    def render(self):
        
        ep = self.inventory.model
        ep.setPos(0,0,0.03)
        ep.reparentTo(self.model)
    
    def clean(self):
        self.inventory.model.removeNode()
    
    def finish_pan_fry(self,name):
        self.clean()
        self.inventory = Ingredient("steak",load_model("steak"))
        self.render()