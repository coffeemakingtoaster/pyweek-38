from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.dish import Dish
from helpers.model_helpers import load_model
from entities.item_base import ItemBase
from entities.ingredient import Ingredient
from entities.salt import Salt
import copy

class Delivery(Station):
    def __init__(self,actor):
        self.id = "Delivery"
        super().__init__(self.id,actor)
        
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        
        self.render()
        
    
    def interact(self,item,player):
        
        
        if self.inventory.id == "empty_hands" and type(item) == Dish and item.finished:
            c_item = copy.deepcopy(item)
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            self.clean()
            self.inventory = c_item
            self.render()
        elif type(self.inventory) == Dish and item.id =="Salt":
            print("Salz?")
            
            if not player.sneaking and not self.inventory.badSalt:
                self.inventory.goodSalt = True
            elif player.sneaking:
                self.inventory.badSalt = True
            
            self.inventory.apply_effects()
                
        elif type(self.inventory) == Dish and item.id =="chopped_chili" and player.sneaking:
            self.inventory.spice = True
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            self.inventory.apply_effects()
            
            
        
    
    
        
    def render(self):
        
        ep = self.inventory.model
        ep.setPos(0,0,0.78)
        ep.reparentTo(self.model)
        
        
    def clean(self):
        self.inventory.model.removeNode()
    