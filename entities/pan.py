from constants.map import TARGETS
from entities.station import Station
from entities.item_base import ItemBase
from entities.dish import Dish
from entities.ingredient import Ingredient
from helpers.model_helpers import load_model
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import *
from entities.progress_bar import ProgressBar

class Pan(Station):
    def __init__(self, actor):
        self.id = TARGETS.PAN
        self.duration = 10  # Frying duration in seconds
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        self.progressBar = None
        self.evil_progressBar = None
        self.evil_task = None
        self.evil_duration = 3
        self.p = None
        self.evil_p = None
        

        super().__init__(self.id, actor)

    def interact(self, item, player):
        if player.sneaking and self.inventory.id == "raw_steak":
            self.evil_progressBar = ProgressBar(self.model,self.evil_duration,1)
            self.evil_p = ParticleEffect()
            self.evil_p.load_config("assets/particles/flame/bad_flame.ptf")
            self.evil_p.start(self.model, self.model)
            self.evil_task = taskMgr.doMethodLater(self.evil_duration, self.burn, "task")
        
        elif item.id == "raw_steak" and self.inventory.id == "empty_hands":
            self.inventory = Ingredient(item.id, load_model(item.id))
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
            self.render()

            self.p = ParticleEffect()
            self.p.loadConfig("assets/particles/flame/flame.ptf")
            self.p.start(self.model, self.model)

            # Initialize the 3D progress bar
            self.progressBar = ProgressBar(self.model,self.duration,0)

            # Start the frying process and setup task to finish after the duration
            self.task = taskMgr.doMethodLater(self.duration, self.finish_pan_fry, "task")
        
        elif (item.id == "empty_hands" or isinstance(item, Dish)) and self.inventory.id == "steak":
            player.set_holding(Ingredient("steak", load_model("steak")))
            self.clean()
            self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
            self.render()

        else:
            # Error Sound
            print("I only cook steak :(")

    def render(self):
        ep = self.inventory.model
        ep.setPos(0, 0, 0.03)
        ep.reparentTo(self.model)

    def clean(self):
        self.inventory.model.removeNode()

    def finish_pan_fry(self,name):
        self.p.disable()  # Stop particle effect
        self.clean()  # Remove the raw steak model
        self.inventory = Ingredient("steak", load_model("steak"))  # Set cooked steak
        self.render()

        # Remove the 3D progress bar when cooking is done
        self.progressBar.destroy()
        self.progressBar = None

        self.task = None
        if self.evil_task:
            self.evil_task = None
            taskMgr.remove(self.evil_task)
            self.evil_p.disable()
            self.evil_progressBar.destroy()
            self.evil_progressBar = None
            
    def burn(self,name):
        self.p.disable()
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
    

   



 

