from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from constants.events import EVENT_NAMES
from entities.station import Station
from entities.dish import Dish
from helpers.model_helpers import load_model
from entities.item_base import ItemBase
from entities.ingredient import Ingredient
from entities.salt import Salt
import copy
from constants.map import TARGETS

class Delivery(Station):
    def __init__(self,actor):
        self.id = TARGETS.DROPOFF
        super().__init__(self.id,actor)
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))

        self.item_was_dropped_off_by_player = False
        
        self.render()

    def interact(self,item,player):
        
        print("HELLLO ITS ME")
        
        if self.inventory.id == "empty_hands" and type(item) == Dish and item.finished:
            c_item = copy.deepcopy(item)
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            self.item_was_dropped_off_by_player = True
            self.inventory = c_item
            taskMgr.do_method_later(10 ,self.clean,"empty_delivery")
            self.render()
        elif type(self.inventory) == Dish and item.id =="Salt":
            
            
            if not player.sneaking and not self.inventory.badSalt:
                self.inventory.goodSalt = True
                
            elif player.sneaking:
                self.inventory.badSalt = True
                
            self.inventory.apply_effects()
            
        
        elif type(self.inventory) == Dish and item.id =="chopped_chili":
            
            
            if player.sneaking and not self.inventory.spiced:
                self.inventory.spiced = True
                
                
            self.inventory.apply_effects()
                
        elif type(self.inventory) == Dish and item.id =="chopped_chili" and player.sneaking:
            self.inventory.spice = True
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            self.inventory.apply_effects()

    def render(self):
        ep = self.inventory.model
        ep.setPos(0,0,0.78)
        ep.reparentTo(self.model)
        
    def clean(self,_=None):
        if not self.inventory is None:
            print(f"currently {self.item_was_dropped_off_by_player}")
            messenger.send(EVENT_NAMES.FINISH_ORDER, [self.inventory, self.item_was_dropped_off_by_player ])
            self.item_was_dropped_off_by_player = False
            if not self.inventory.model is None:
                self.inventory.model.removeNode()
            self.inventory= (ItemBase("empty_hands", load_model("empty_hands")))
    
