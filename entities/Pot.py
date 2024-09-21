from json import load
from direct.actor.Actor import Actor

from constants.map import TARGETS
from entities.station import Station
from entities.item_base import ItemBase
from entities.dish import Dish
from entities.ingredient import Ingredient
from helpers.model_helpers import load_3d_sounds, load_model
from entities.progress_bar import ProgressBar
import copy

class Pot(Station):
    def __init__(self,actor: Actor):
        self.id = TARGETS.POT 
        self.duration = 10
        self.progressBar = None
        self.ingredients = []
        self.inventory = ItemBase("empty_hands",load_model("empty_hands"))
        
        self.evil_progressBar = None
        self.evil_task = None
        self.evil_duration = 3
        
        super().__init__(self.id,actor)

        self.sounds = load_3d_sounds("pot", self.model)
    
    def interact(self,item,player):
        if type(self.inventory) == Dish and item.id =="Salt":
            if not player.sneaking and not self.inventory.badSalt:
                self.inventory.goodSalt = True
                self.inventory.apply_effects()
            elif player.sneaking:
                self.evil_progressBar = ProgressBar(self.model,self.evil_duration,1,player)
                self.evil_task = taskMgr.doMethodLater(self.evil_duration, self.salt, "task")
                   
        elif type(self.inventory) == Dish and item.id =="chopped_chili" and player.sneaking and not self.inventory.spiced:
            self.evil_progressBar = ProgressBar(self.model,self.evil_duration,1,player)
            self.evil_task = taskMgr.doMethodLater(self.evil_duration, self.spice, "task",extraArgs = [player])
            self.inventory.apply_effects()
        elif (item.id == "chopped_potatoes" or item.id == "chopped_onion") and self.inventory is not "unplated_soup":
            if item.id not in self.ingredients:
                self.ingredients.append(item.id)
                player.set_holding(ItemBase("empty_hands",load_model("empty_hands")))
            if len(self.ingredients) == 2:
                self.inventory = Dish("unplated_soup",load_model("plated_soup"))
                self.render()
                self.progressBar = ProgressBar(self.model,self.duration,0,player)
                self.play_sound(True)
                self.task = taskMgr.do_method_later(self.duration,self.finish_soup,"task")
        elif item.id == "empty_plate" and self.inventory.id == "plated_soup":
            player.hardset(copy.deepcopy(self.inventory))
            player.holding.apply_effects()
            self.clean()
        else:
            self.play_error_sound()
           
    def finish_soup(self,name):
        self.stop_sound()
        self.inventory.id = "plated_soup"
        self.inventory.finished = True
        self.render()
        self.task = None
        if self.progressBar:
            self.progressBar.destroy()
            self.progressBar = None
        
        

    def render(self):
        
        ep = self.inventory.model
        ep.setPos(0,0,0)
        ep.reparentTo(self.model)
        
    def clean(self):
        
        self.inventory.model.removeNode()
        self.ingredients = []
        self.inventory = ItemBase("empty_hands",load_model("empty_hands"))


    def salt(self,name):
        self.inventory.badSalt = True
        self.inventory.apply_effects()
        self.evil_task = None
        self.evil_progressBar.destroy()
        self.evil_progressBar = None
    
    def spice(self,player):
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
