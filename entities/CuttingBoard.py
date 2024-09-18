from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.dish import Dish
from helpers.model_helpers import load_model
from entities.item_base import ItemBase
from entities.ingredient import Ingredient

class CuttingBoard(Station):
    def __init__(self,actor):
        self.id = "CuttingBoard"
        
        self.inventory = None
        self.cuttables = ["tomato","potato","cheese","chocolate","salad","onion"]
        self.cuts = ["chopped_tomato","chopped_potato","chopped_cheese","chopped_chocolate","chopped_salad","chopped_onion"]
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if item.id == "empty_hands" and self.inventory.id in self.cuts:
            player.set_holding(self.inventory)
            
            self.inventory = None
            return True
        elif item.id in self.cuttables and self.inventory is None:
            self.inventory = Ingredient(item.id,load_model(item.id))
            self.render()
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            return True
        elif item.id == "empty_hands" and self.inventory.id in self.cuttables:
            self.model.play("Cut")
            #TODO: Wait
            cuttable_id = self.cuts[self.cuttables.index(self.inventory.id)]
            self.clean()
            self.inventory = Ingredient(cuttable_id,load_model(cuttable_id))
            self.render()
            
            return True
        return False
    
    
        
    def render(self):
        
        ep = self.inventory.model
        ep.setPos(0,0,0.78)
        ep.reparentTo(self.model)
        
        
    def clean(self):
        self.inventory.model.removeNode()
    