from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from constants.map import TARGETS
from entities.station import Station
from entities.dish import Dish
from helpers.model_helpers import load_model
from entities.item_base import ItemBase
from entities.ingredient import Ingredient
from entities.progress_bar import ProgressBar
import copy


class CuttingBoard(Station):
    def __init__(self,actor):
        self.id = TARGETS.CUTTING_BOARD
        self.progressBar = None
        self.duration = 2

        self.is_cutting = False
        
        self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        self.cuttables = ["tomato","potato","cheese","chocolate","salad","onion","Chili"]
        self.cuts = ["chopped_tomato","chopped_potatoes","chopped_cheese","chopped_chocolate","chopped_salad","chopped_onion","chopped_chili"]
        super().__init__(self.id,actor)
    
    def interact(self,item,player):
        print(item.id)
        
        #Picking Up Stuff from board
        if item.id == "empty_hands" and self.inventory.id in self.cuts:
            player.set_holding(Ingredient(self.inventory.id,load_model(self.inventory.id)))
            self.clean()
            self.inventory = ItemBase("empty_hands", load_model("empty_hands"))
        #Placing Stuff on Plate
        elif item.id in self.cuttables and self.inventory.id == "empty_hands":
            self.inventory = Ingredient(item.id,load_model(item.id))
            self.render()
            player.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
        #Cutting Stuff
        elif item.id == "empty_hands" and self.inventory.id in self.cuttables:
            self.model.play("Cut")
            self.is_cutting = True 
            self.progressBar = ProgressBar(self.model,self.duration,0)
            self.task = taskMgr.do_method_later(self.duration,self.finish_cut,"task")
            # should block
        elif type(self.inventory) == Ingredient and type(item) == Dish:
            if player.set_holding(self.inventory):
                player.holding.apply_effects()
                self.clean()
                self.inventory=(ItemBase("empty_hands", load_model("empty_hands")))
                self.render()
        
        elif item.id in self.cuttables:
            self.swap(item,player)
            
    def render(self):
        
        ep = self.inventory.model
        ep.setPos(0,0,0.03)
        ep.reparentTo(self.model)
        
        
    def clean(self):
        self.inventory.model.removeNode()
        
    def finish_cut(self,name):
        cuttable_id = self.cuts[self.cuttables.index(self.inventory.id)]
        self.is_cutting = False
        self.clean()
        self.inventory = Ingredient(cuttable_id,load_model(cuttable_id))
        self.render()
        self.progressBar.destroy()
        self.progressBar = None
        self.task = None
    
    def unset_interact(self,palyer):
        
        if self.task is not None:
            
            taskMgr.remove(self.task)
            self.progressBar.destroy()
            self.progressBar = None
            self.model.stop()
            
    def swap(self,item,player):
        c_item = copy.deepcopy(item)
        c_inv = copy.deepcopy(self.inventory)
        c_inv.apply_effects()
        self.clean()
        player.hardset(c_inv)
        self.inventory = c_item
        self.render()
