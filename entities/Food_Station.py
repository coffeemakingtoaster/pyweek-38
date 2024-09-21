from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station
from entities.dish import Dish
from entities.ingredient import Ingredient
from helpers.model_helpers import load_3d_sounds, load_model

class Food_Station(Station):
    def __init__(self,actor,name,food_id):
        self.id = name
        self.food_id = food_id
        self.inventory = [Ingredient(food_id,load_model(food_id)),Ingredient(food_id,load_model(food_id))]
        
        super().__init__(self.id,actor)

        self.sounds = load_3d_sounds("grab", self.model)
    
    def interact(self,item,player):
        
        if item.id == "empty_hands" and self.inventory[0] is not None:
            player.set_holding(Ingredient(self.food_id,load_model(self.food_id)))
            self.play_sound()
            return True
        self.play_error_sound()
        return False
