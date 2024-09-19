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
        
        self.duration = 2
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        self.cuttables = ["tomato","potato","cheese","chocolate","salad","onion"]
        self.cuts = ["chopped_tomato","chopped_potatoes","chopped_cheese","chopped_chocolate","chopped_salad","chopped_onion"]
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        print(item.id)
        
        
        #Picking Up Stuff from board
        if item.id == "empty_hands" and self.inventory.id in self.cuts:
            player.set_holding(Ingredient(self.inventory.id,load_model(self.inventory.id)))
            self.clean()
            self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
            return True
        #Placing Stuff on Plate
        elif item.id in self.cuttables and self.inventory.id == "empty_hands":
            self.inventory = Ingredient(item.id,load_model(item.id))
            self.render()
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            return True
        #Cutting Stuff
        elif item.id == "empty_hands" and self.inventory.id in self.cuttables:
            self.model.play("Cut")
            #TODO: Wait
            self.task = taskMgr.do_method_later(self.duration,self.finish_cut,"task")
        elif type(self.inventory) == Ingredient and type(item) == Dish:
            if player.set_holding(self.inventory):
                self.clean()
                self.inventory=(ItemBase("empty_hands", load_model("empty_hands")))
                self.render()
        
        elif item.id in self.cuttables:
            player.set_holding(type(self.inventory)(self.inventory.id,load_model(self.inventory.id)))
            self.clean()
            self.inventory = type(item)(item.id,load_model(item.id))
            self.render()
            return True    
            
        return False
    
    
        
    def render(self):
        
        ep = self.inventory.model
        ep.setPos(0,0,0.03)
        ep.reparentTo(self.model)
        
        
    def clean(self):
        self.inventory.model.removeNode()
        
    def finish_cut(self,name):
        cuttable_id = self.cuts[self.cuttables.index(self.inventory.id)]
        self.clean()
        self.inventory = Ingredient(cuttable_id,load_model(cuttable_id))
        self.render()
        self.task = None
    
