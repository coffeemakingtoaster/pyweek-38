from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from constants.events import EVENT_NAMES
from entities.station import Station
from entities.dish import Dish
from helpers.model_helpers import load_3d_sounds, load_model
from entities.item_base import ItemBase
from entities.ingredient import Ingredient
from entities.salt import Salt
import copy
from constants.map import TARGETS
from entities.progress_bar import ProgressBar

class Delivery(Station):
    def __init__(self,actor):
        self.id = TARGETS.DROPOFF
        super().__init__(self.id,actor)
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))

        self.item_was_dropped_off_by_player = False
        
        self.render()
        self.evil_progressBar = None
        self.evil_task = None
        self.evil_duration = 3
        self.sounds = load_3d_sounds("dish_delivery", self.model)

    def interact(self,item,player):
        
        if self.inventory.id == "empty_hands" and type(item) == Dish and item.finished:
            c_item = copy.deepcopy(item)
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            self.item_was_dropped_off_by_player = player.id == "player"
            self.inventory = c_item
            self.play_sound()
            taskMgr.do_method_later(10 ,self.clean,"empty_delivery")
            self.render()
        
        if type(self.inventory) == Dish and item.id =="Salt":
            
            
            if not player.sneaking and not self.inventory.badSalt:
                
                self.inventory.goodSalt = True
                self.inventory.apply_effects()
                
            elif player.sneaking:
                
                self.evil_progressBar = ProgressBar(self.model,self.evil_duration,1,player)
                self.evil_task = taskMgr.doMethodLater(self.evil_duration, self.salt, "task")
                   
        elif type(self.inventory) == Dish and item.id =="chopped_chili" and player.sneaking and not self.inventory.spiced:
            self.evil_progressBar = ProgressBar(self.model,self.evil_duration,1,player)
            self.evil_task = taskMgr.doMethodLater(self.evil_duration, self.spice, "task")


    def render(self):
        ep = self.inventory.model
        ep.setPos(0,0,0.78)
        ep.reparentTo(self.model)
        
    def clean(self,_=None):
        self.stop_sound()
        if not self.inventory is None:
            print(f"currently {self.item_was_dropped_off_by_player}")
            messenger.send(EVENT_NAMES.FINISH_ORDER, [self.inventory, self.item_was_dropped_off_by_player ])
            self.item_was_dropped_off_by_player = False
            if not self.inventory.model is None:
                self.inventory.model.removeNode()
            self.inventory= (ItemBase("empty_hands", load_model("empty_hands")))
    def salt(self,name):
        self.inventory.badSalt = True
        self.inventory.apply_effects()
        self.evil_task = None
        self.evil_progressBar.destroy()
        self.evil_progressBar = None
    
    def spice(self,name):
        self.inventory.spiced = True
        player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
        self.inventory.apply_effects()
        self.evil_task = None
        self.evil_progressBar.destroy()
        self.evil_progressBar = None
        
    
    def unset_interact(self,player):
        if self.evil_task:
            self.evil_progressBar.destroy()
            self.evil_progressBar = None
            
            taskMgr.remove(self.evil_task)
            self.evil_task = None
