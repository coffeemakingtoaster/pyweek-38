from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from constants.map import TARGETS
from entities.station import Station
from entities.dish import Dish
from helpers.model_helpers import load_model
from entities.item_base import ItemBase
from entities.ingredient import Ingredient

class ItemArea(Station):
    def __init__(self,actor):
        self.id = TARGETS.COUNTERTOP
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if type(self.inventory) == Dish and type(item) == Ingredient:
            if self.inventory.add_ingredient(item.id):
                self.inventory.model.reparentTo(self.model)
                player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            else:
                player.set_holding(type(self.inventory)(self.inventory.id,load_model(self.inventory.id)))
                self.clean()
                self.inventory = type(item)(item.id,load_model(item.id))
                self.render()
                return True
        elif type(self.inventory) == Ingredient and type(item) == Dish:
            if player.set_holding(self.inventory):
                self.clean()
                self.inventory=(ItemBase("empty_hands", load_model("empty_hands")))
                self.render()
            else:
                player.hardset(type(self.inventory)(self.inventory.id,load_model(self.inventory.id)))
                self.clean()
                self.inventory = type(item)(item.id,load_model(item.id))
                self.render()
                
        else:
            print("Hello Edgecase")
            player.set_holding(type(self.inventory)(self.inventory.id,load_model(self.inventory.id)))
            self.clean()
            self.inventory = type(item)(item.id,load_model(item.id))
            self.render()
            return True
    
    
        
    def render(self):
        
        ep = self.inventory.model
        ep.setPos(0,0,0.78)
        ep.reparentTo(self.model)
        
        
    def clean(self):
        self.inventory.model.removeNode()
    
