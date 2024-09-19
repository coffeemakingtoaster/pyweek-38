from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point3, CollisionNode, CollisionSphere

import math

from constants.layers import VIEW_COLLISION_BITMASK
from constants.player_const import MOVEMENT
from entities import station
from entities.dish import Dish
from entities.entity_base import EntityBase
from constants import player_const
from entities.item_base import ItemBase
from helpers.math_helper import get_first_intersection, get_limited_rotation_target
from helpers.model_helpers import load_particles, load_model
from helpers.pathfinding_helper import global_pos_to_grid, grid_pos_to_global


class Player(EntityBase):
    def __init__(self,stations):
        super().__init__()

        self.id = "player"
        self.stations = stations
        self.move_speed = MOVEMENT.PLAYER_MOVEMENT_SPEED
        self.movement_status = {"up": 0, "down": 0, "left": 0, "right": 0}
        self.holding = ItemBase("empty_hands", load_model("empty_hands"))
        

        # Keybinds for movement
        self.accept("a", self.set_movement_status, ["left"])
        self.accept("a-up", self.unset_movement_status, ["left"])
        self.accept("d", self.set_movement_status, ["right"])
        self.accept("d-up", self.unset_movement_status, ["right"])
        self.accept("w", self.set_movement_status, ["up"])
        self.accept("w-up", self.unset_movement_status, ["up"])
        self.accept("s", self.set_movement_status, ["down"])
        self.accept("s-up", self.unset_movement_status, ["down"])

        self.accept("e", self.set_interact)
        self.accept("e-up", self.unset_interact)

        self.model = Actor("assets/models/MapObjects/Player/Player.bam",
                           {"Walk": "assets/models/MapObjects/Player/Player-Walk.bam"})
        self.model.setPos(0, 0, MOVEMENT.PLAYER_FIXED_HEIGHT)
        self.model.reparentTo(render)

        self.walk_particles = load_particles("dust")
        self.walk_particles_active = False
        self.__add_player_collider()
        self.holding.model.setPos(0, -0.4, 0.76)
        self.holding.model.reparentTo(self.model)
        #self.model.loop("Walk")

    def __add_player_collider(self):
        self.hitbox = self.model.attachNewNode(CollisionNode("player_hitbox"))
        self.hitbox.setCollideMask(VIEW_COLLISION_BITMASK)
        #self.hitbox.show()
        self.hitbox.setPos(0, 0, 0)
        self.hitbox.node().addSolid(CollisionSphere(Point3(0, 0, 0), 1))

    def set_movement_status(self, direction):
        self.movement_status[direction] = 1

    def unset_movement_status(self, direction):
        self.movement_status[direction] = 0

    def set_interact(self):
        self.find_station().interact(self.holding,self)
        #self.set_holding(Dish("empty_plate", load_model("empty_plate")))
        #print("Interacting.")

    def unset_interact(self):
        return
        #print("Disabling interact.")

    def set_holding(self, new_item):
        
        if type(self.holding) == Dish and new_item.id is not "empty_hands" and type(new_item) is not Dish :
            
            if self.holding.add_ingredient(new_item.id):
                self.holding.model.reparentTo(self.model)
                return True
            else:
                return False
            

        else:
            self.hardset(new_item)

            # ep = load_model("empty_plate")
            # ep.reparentTo(self.model)
            # ep.setPos(2, 0, 2)

    def hardset(self,item):
        self.holding.model.removeNode()

        ep = item.model
        print(item.model)
        ep.reparentTo(self.model)

        ep.setPos(0, -0.5, 0.76)
        self.holding = item
        
    def find_station(self):
        point = self.holding.model.getPos(render)
        lowest_distance = 200
        closest_station = None
        
        for station in self.stations:
            if (station.model.getPos() - point).length() < lowest_distance:
                lowest_distance = (station.model.getPos() - point).length()
                closest_station = station
        
        print(closest_station.model.getPos())
        return closest_station
                
    def update(self, dt):
        
        self.model.node().resetAllPrevTransform()

        movement_direction = Vec3(
            ((self.movement_status["left"] * -1) + self.movement_status["right"]) * self.move_speed * dt,
            ((self.movement_status["down"] * -1) + self.movement_status["up"]) * self.move_speed * dt,
            0
        )
        
        if movement_direction.length() > 0:
            target_rotation = math.degrees(math.atan2(movement_direction.x, -movement_direction.y))

            self.model.setH(
                get_limited_rotation_target(
                    self.model.getH(),
                    target_rotation,
                    player_const.MOVEMENT.PLAYER_MAX_TURN_SPEED_DEGREES * dt
                )
            )
            movement_direction = self.__adapt_movement_to_collision(movement_direction)

        self.model.setFluidPos(
            self.model.getX() + movement_direction.x,
            self.model.getY() + movement_direction.y,
            player_const.MOVEMENT.PLAYER_FIXED_HEIGHT
        )

        # Pathfinding mapping debug log
        # print(f"Player: {self.model.getPos()} {global_pos_to_grid(self.model.getPos())} {grid_pos_to_global(global_pos_to_grid(self.model.getPos()))}")
    
    def __adapt_movement_to_collision(self, movement_direction): 
        if (collision := get_first_intersection(self.model.getPos() + Point3(0,0,0.5), movement_direction)) is not None:
            movement_direction = movement_direction.normalized() * min(
                (collision.getSurfacePoint(render) - self.model.getPos()).length() - 0.6, movement_direction.length()
            )
        return movement_direction


    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()
