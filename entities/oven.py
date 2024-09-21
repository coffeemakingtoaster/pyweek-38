from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.item_base import ItemBase
from entities.dish import Dish
from entities.ingredient import Ingredient
from helpers.model_helpers import load_model
import copy
from entities.progress_bar import ProgressBar

class Oven(Station):
    def __init__(self,actor):
        self.id = "Oven"
        self.duration = 10
        self.progressBar = None
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if item.id == "raw_pizza":
            print("Yay Pizza")
            self.inventory = copy.deepcopy(item)
            self.play_anim("Open")
            self.progressBar = ProgressBar(self.model,self.duration,0)
            self.task = taskMgr.do_method_later(1,self.close_door,"task",extraArgs = [player])
        elif item.id == "empty_hands" and self.inventory.id == "plated_pizza":
            player.hardset(copy.deepcopy(self.inventory))
            player.holding.apply_effects()
            self.play_anim("Close")
            self.clean()
        
        
        else:
            #Error Sound
            print("I only eat pizza :()")
            
    def finish_bake(self,name):
        self.inventory.id = "plated_pizza"
        self.inventory.model = load_model("plated_pizza")
        self.inventory.finished = True
        self.play_anim("Open")
        self.task = None
        self.progressBar.destroy()
        self.progressBar = None
    def close_door(self,player):
        self.play_anim("Close")
        player.set_holding(ItemBase("empty_hands",load_model("empty_hands")))
        self.task = taskMgr.do_method_later(self.duration,self.finish_bake,"task")
    def clean(self):
        self.inventory.model.removeNode()
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
                
