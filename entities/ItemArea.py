from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from constants.map import TARGETS
from entities.station import Station
from entities.dish import Dish
from helpers.model_helpers import load_model
from entities.item_base import ItemBase
from entities.ingredient import Ingredient
from entities.salt import Salt
from direct.particles.ParticleEffect import ParticleEffect
import copy
from entities.progress_bar import ProgressBar


class ItemArea(Station):
    def __init__(self,actor):
        self.id = TARGETS.COUNTERTOP
        super().__init__(self.id,actor)
        
        
        self.evil_progressBar = None
        self.evil_task = None
        self.evil_duration = 3
       
        
        
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        
        self.render()
        
    
    def interact(self,item,player):
        
        
        
        if type(self.inventory) == Dish and item.id =="Salt":
            
            
            if not player.sneaking and not self.inventory.badSalt:
                
                self.inventory.goodSalt = True
                self.inventory.apply_effects()
                
            elif player.sneaking:
                
                self.evil_progressBar = ProgressBar(self.model,self.evil_duration,1,player)
                self.evil_task = taskMgr.doMethodLater(self.evil_duration, self.salt, "task")
                   
        elif type(self.inventory) == Dish and item.id =="chopped_chili" and player.sneaking and not self.inventory.spice:
            self.evil_progressBar = ProgressBar(self.model,self.evil_duration,1,player)
            self.evil_task = taskMgr.doMethodLater(self.evil_duration, self.pice, "task")
            
        elif type(self.inventory) == Dish and type(item) == Ingredient:
            if self.inventory.add_ingredient(item.id):
                self.inventory.model.reparentTo(self.model)
                self.inventory.apply_effects()
                player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            else:
                self.swap(item,player)
                return True
        elif type(self.inventory) == Ingredient and type(item) == Dish:
            if player.set_holding(self.inventory):
                player.holding.apply_effects()
                self.clean()
                self.inventory=(ItemBase("empty_hands", load_model("empty_hands")))
                self.render()
            else:
                self.swap(item,player)
                
        else:
            self.swap(item,player)
            return True
    
    
        
    def render(self):
        
        ep = self.inventory.model
        ep.setPos(0,0,0.78)
        ep.reparentTo(self.model)
        
        
    def clean(self):
        self.inventory.model.removeNode()
    
    def swap(self,item,player):
        c_item = copy.deepcopy(item)
        c_inv = copy.deepcopy(self.inventory)
        c_inv.apply_effects()
        self.clean()
        player.hardset(c_inv)
        self.inventory = c_item
        self.render()
        
    def salt(self,name):
        self.inventory.badSalt = True
        self.inventory.apply_effects()
        self.evil_task = None
        self.evil_progressBar.destroy()
        self.evil_progressBar = None
    
    def spice(self,name):
        self.inventory.spice = True
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
     