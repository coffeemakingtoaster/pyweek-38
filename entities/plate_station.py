from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from constants.map import TARGETS
from entities.station import Station
from entities.dish import Dish
from helpers.model_helpers import load_3d_sounds, load_model

class Plate_Station(Station):
    def __init__(self,actor):
        self.id = TARGETS.WASHER 
        
        self.inventory = [Dish("empty_plate",load_model("empty_plate")),Dish("empty_plate",load_model("empty_plate"))]
        
        super().__init__(self.id,actor)

        self.sounds = load_3d_sounds("plates",self.model)
    
    def interact(self,item,player):
        
        if item.id == "empty_hands":
            player.set_holding(Dish("empty_plate",load_model("empty_plate")))
            self.play_sound()
            return True
        self.play_error_sound()
        return False
