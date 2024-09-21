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
from direct.particles.ParticleEffect import ParticleEffect

class Fry(Station):
    def __init__(self,actor):
        self.id = TARGETS.FRY 
        self.duration = 10
        self.progressBar = None
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        self.evil_progressBar = None
        self.evil_task = None
        self.evil_duration = 3
        self.evil_p = None
        
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        
        if player.sneaking and self.inventory.id == "chopped_potatoes" and item.id == "ice_cubes":
            self.evil_progressBar = ProgressBar(self.model,self.evil_duration,1)
            self.evil_p = ParticleEffect()
            self.evil_p.load_config("assets/particles/flame/bad_flame.ptf")
            self.evil_p.start(self.model, self.model)
            self.evil_task = taskMgr.doMethodLater(self.evil_duration, self.burn, "task")
        
        elif item.id == "chopped_potatoes":
            print("potatoes!!!")
            
            
            self.model.loop("Fry")
            self.inventory = Ingredient(item.id, load_model(item.id))
            self.progressBar = ProgressBar(self.model,self.duration,0)
            self.task = taskMgr.do_method_later(self.duration,self.fry,"task")
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
        elif (item.id == "empty_hands" or type(item) == Dish) and  self.inventory.id == "fries":
            player.set_holding(Ingredient("fries",load_model("fries")))
            
        
        
        else:
            #Error Sound
            print("I only eat fries :()")
            
    def fry(self,name):
        self.inventory = Ingredient("fries",load_model("fries"))
        self.model.stop()
        self.task = None
        self.progressBar.destroy()
        self.progressBar = None
        
        if self.evil_task:
            self.evil_task = None
            taskMgr.remove(self.evil_task)
            self.evil_p.disable()
            self.evil_progressBar.destroy()
            self.evil_progressBar = None
        
    def burn(self,name):
        self.model.stop()
        self.evil_p.disable()
        self.clean()  
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        self.render()

        # Remove the 3D progress bar when cooking is done
        self.progressBar.destroy()
        self.progressBar = None
        self.evil_progressBar.destroy()
        self.evil_progressBar = None

        taskMgr.remove(self.task)
        self.task = None
        self.evil_task = None

    def unset_interact(self,player):
        if self.evil_task:
            self.evil_progressBar.destroy()
            self.evil_progressBar = None
            self.evil_p.disable()
            taskMgr.remove(self.evil_task)
            self.evil_task = None
    
    def render(self):
        ep = self.inventory.model
        ep.setPos(0, 0, 0.03)
        ep.reparentTo(self.model)

    def clean(self):
        self.inventory.model.removeNode()