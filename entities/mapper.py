from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
import os

from constants.player_const import MOVEMENT
from entities.entity_base import EntityBase
from constants import player_const
from helpers.math_helper import get_limited_rotation_target
from helpers.model_helpers import load_particles
from helpers.model_helpers import load_model
from entities.map_loader import load_map
import json


class Mapper(EntityBase):
    def __init__(self):
        super().__init__()
        
        with open('./map.json', 'r') as file:
            data = json.load(file)
        
        self.map = load_map(data)
        for obj in self.map:
            obj.reparentTo(render)
        
        self.models = []
        self.target_rotation = 0
        self.current_model_index = 0
        
        self.model = None

        self.id = "player"
        self.move_speed = MOVEMENT.PLAYER_MOVEMENT_SPEED
        self.movement_status = {"up": 0, "down": 0, "left": 0, "right": 0}
        self.turn_status = {"up": 0, "down": 0}

        # Keybinds for movement
        self.accept("a", self.set_movement_status, ["left"])
        self.accept("a-up", self.unset_movement_status, ["left"])
        self.accept("d", self.set_movement_status, ["right"])
        self.accept("d-up", self.unset_movement_status, ["right"])
        self.accept("w", self.set_movement_status, ["up"])
        self.accept("w-up", self.unset_movement_status, ["up"])
        self.accept("s", self.set_movement_status, ["down"])
        self.accept("s-up", self.unset_movement_status, ["down"])
        
        self.accept("o", self.set_turn_status, ["up"])
        self.accept("o-up", self.unset_turn_status, ["up"])
        self.accept("p", self.set_turn_status, ["down"])
        self.accept("p-up", self.unset_turn_status, ["down"])
        self.accept("l", self.turn45)
        self.accept("m",self.save_and_more)
        self.accept("n",self.save_and_next)
        self.accept("v",self.next)
        self.accept("b",self.back)

        self.accept("e", self.set_interact)
        self.accept("e-up", self.unset_interact)

        self.load_models()
        print(self.models)

        #self.model = Actor("assets/models/Player/Player.bam", {"Idle": "assets/models/Player/Player.bam"})
        #self.model.setPos(0, 0, 0)
        #self.model.reparentTo(render)

        #self.walk_particles = load_particles("dust")
        #self.walk_particles_active = False
        
        self.model = load_model(self.models[self.current_model_index])
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(render)

    def set_movement_status(self, direction):
        self.movement_status[direction] = 1

    def unset_movement_status(self, direction):
        self.movement_status[direction] = 0
    
    def set_turn_status(self, direction):
        self.turn_status[direction] = 1

    def unset_turn_status(self, direction):
        self.turn_status[direction] = 0   
    def turn45(self):
        self.model.setH(self.model.getH() + 45)
        
    def next(self):
        
        self.model.removeNode()
        self.current_model_index += 1
        if self.current_model_index >= len(self.models):
            self.current_model_index = 0
        self.model = load_model(self.models[self.current_model_index])
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(render)
    
    def back(self):
        
        self.model.removeNode()
        self.current_model_index += -1
        if self.current_model_index <= 0:
            self.current_model_index = len(self.models)-1
        self.model = load_model(self.models[self.current_model_index])
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(render)
    
    def save_and_next(self):
        self.save_model_data()
        self.current_model_index += 1
        if self.current_model_index >= len(self.models):
            self.current_model_index = 0
        self.model = load_model(self.models[self.current_model_index])
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(render)
    
    def save_and_more(self):
        self.save_model_data()
        self.model = load_model(self.models[self.current_model_index])
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(render)
        
    #def save_and_more(self):
        
    def load_models(self):
        for root, dirs, files in os.walk("assets/models"):
            for file in files:
                if '-' not in file:
                    model_name = os.path.splitext(file)[0]
                    self.models.append(model_name)
                       
    
    def save_model_data(self):
        # Get the model name, position, and rotation
        model_name = self.models[self.current_model_index]
        position = self.model.getPos()
        rotation = self.model.getH()

        # Create an object to store this data
        model_data = {
            "name": model_name,
            "position": {
                "x": position.getX(),
                "y": position.getY(),
                "z": position.getZ()
            },
            "rotation": rotation
        }

        # Load existing data
        with open('./map.json', 'r') as file:
            data = json.load(file)

        # Append the new model data
        data['Objects'].append(model_data)

        # Save the updated data
        with open('./map.json', 'w') as file:
            json.dump(data, file, indent=4)        
            
        
    

    def set_interact(self):
        print("Interacting.")

    def unset_interact(self):
        print("Disabling interact.")

    def update(self, dt):
        self.model.node().resetAllPrevTransform()

        movement_direction = Vec3(
            ((self.movement_status["left"] * -1) + self.movement_status["right"]) * 5 * dt,
            ((self.movement_status["down"] * -1) + self.movement_status["up"]) * 5 * dt,
            0
        )
        
        
        

        

        self.model.setH(self.model.getH() + ((self.turn_status["up"] * -1) + self.turn_status["down"]) * 20 * dt)
            

        

        self.model.setPos(
            self.model.getX() + movement_direction.x,
            self.model.getY() + movement_direction.y,
            player_const.MOVEMENT.PLAYER_FIXED_HEIGHT
        )

    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()
