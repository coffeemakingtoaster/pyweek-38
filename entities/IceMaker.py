from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from constants.map import TARGETS
from entities.station import Station
from entities.item_base import ItemBase
from entities.dish import Dish
from entities.ingredient import Ingredient
from helpers.model_helpers import load_model
from entities.progress_bar import ProgressBar
import copy

class IceMaker(Station):
    def __init__(self,actor):
        self.id = TARGETS.ICEMAKER
        self.duration = 10
        self.progressBar = None
        self.ingredients = []
        self.inventory = ItemBase("empty_hands",load_model("empty_hands"))
        
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if type(self.inventory) == Dish and item.id =="Salt":
            
            
            if not player.sneaking and not self.inventory.badSalt:
                self.inventory.goodSalt = True
                
            elif player.sneaking:
                self.inventory.badSalt = True
                
            self.inventory.apply_effects()
        elif type(self.inventory) == Dish and item.id =="chopped_chili":
            
            
            if player.sneaking and not self.inventory.spiced:
                self.inventory.spiced = True
                player.set_holding(ItemBase("empty_hands",load_model("empty_hands")))
                
                
            self.inventory.apply_effects()
        
        elif (item.id == "ice_cubes" or item.id == "chopped_chocolate")and self.inventory.id is not "unplated_ice_cream" and len(self.ingredients) is not 2:
            if item.id not in self.ingredients:
                print("Yay" + item.id)
                self.ingredients.append(item.id)
                player.set_holding(ItemBase("empty_hands",load_model("empty_hands")))
            if len(self.ingredients) == 2:
                self.play_anim("Close")
                self.inventory = Dish("unplated_ice_cream",load_model("plated_ice_cream"))
                self.render()
                self.progressBar = ProgressBar(self.model,self.duration,0)
                self.task = taskMgr.do_method_later(self.duration,self.finish_ice,"task")
        elif item.id == "empty_plate" and self.inventory.id == "plated_ice_cream":
            player.hardset(copy.deepcopy(self.inventory))
            player.holding.apply_effects()
            self.clean()
            
        else:
            #Error Sound
            print("I only eat pizza :()")
            
    def finish_ice(self,name):
        self.inventory.id = "plated_ice_cream"
        self.play_anim("Open")
        self.task = None
        self.progressBar.destroy()
        self.progressBar = None
                
    def render(self):
        
        ep = self.inventory.model
        ep.setPos(0,0,-2)
        ep.reparentTo(self.model)
        
    def clean(self):
        
        self.inventory.model.removeNode()
        self.ingredients = []
        self.inventory = ItemBase("empty_hands",load_model("empty_hands"))