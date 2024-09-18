import math

from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point2, CollisionNode, CollisionBox, Point3, CollisionHandlerEvent, CollisionEntry

from entities.entity_base import EntityBase
from constants.enemy_const import MOVEMENT
from helpers.math_helper import get_limited_rotation_target
from helpers.model_helpers import load_particles

import random
import uuid

from helpers.pathfinding_helper import get_path_from_to_tile_type, global_pos_to_grid, grid_pos_to_global

__POSSIBLE_TARGETS = ['A','B']

class Enemy(EntityBase):
    def __init__(self, spawn_x, spawn_y, target = "A"):
        super().__init__()
        self.id = f"enemy-{str(uuid.uuid4())}"
        self.move_speed = MOVEMENT.ENEMY_MOVEMENT_SPEED

        self.model = Actor("assets/models/MapObjects/Oven/Oven.bam", {"Idle": "assets/models/MapObjects/Oven/Oven.bam"})
        self.model.setPos(spawn_x, spawn_y, MOVEMENT.ENEMY_FIXED_HEIGHT)

        self.model.reparentTo(render)

        self.__spawn_viewcone()
        self.walk_particles = load_particles("dust")
        self.walk_particles_active = False
        self.target = target 
        self.waypoints = get_path_from_to_tile_type(global_pos_to_grid(self.model.getPos()),self.target) 
        self.desired_pos = grid_pos_to_global(self.waypoints.pop(0))

    def __spawn_viewcone(self):
        # setup hitboxes
        self.viewcone = self.model.attachNewNode(CollisionNode("enemy_viewcone"))
        self.viewcone.show()
        self.viewcone.setPos(0, 0, 0)
        self.viewcone.node().addSolid(CollisionBox(Point3(0.5, 0.5, 0.5), 1, 1, 1))
        # setup notifier
        self.notifier = CollisionHandlerEvent()
        self.notifier.addInPattern(f"{self.id}-into-%in")
        self.notifier.addOutPattern(f"{self.id}-out-%in")

        base.cTrav.addCollider(self.viewcone, self.notifier)
        # setup collision handlers
        self.accept(f"{self.id}-into-player_hitbox", self.__handle_player_enter_viewcone)
        self.accept(f"{self.id}-out-player_hitbox", self.__handle_player_leave_viewcone)

    def __handle_player_enter_viewcone(self, _: CollisionEntry):
        print(f"I ({self.id}) see the player")

    def __handle_player_leave_viewcone(self, _: CollisionEntry):
        print(f"I ({self.id}) lost him")

    def update(self, dt):
        self.model.node().resetAllPrevTransform()
        current_pos = self.model.getPos()
        delta_to_end = Vec3(current_pos.x - self.desired_pos.x, current_pos.y - self.desired_pos.y, 2)
        normalized = Point2(delta_to_end.x, delta_to_end.y).normalized()

        x_direction = normalized.x * self.move_speed * dt
        y_direction = normalized.y * self.move_speed * dt

        if delta_to_end.length() <= 0.5:
            x_direction = 0
            y_direction = 0
            if len(self.waypoints) == 0:
                if self.target == "B":
                    self.target = "A"
                else:
                    self.target = "B"
                self.waypoints = get_path_from_to_tile_type(global_pos_to_grid(self.model.getPos()),self.target, True) 
            self.desired_pos = grid_pos_to_global(self.waypoints.pop(0))

        if delta_to_end.length() > 3:
            target_rotation = math.degrees(math.atan2(delta_to_end.x, -delta_to_end.y)) 

            self.model.setH(
                get_limited_rotation_target(
                    self.model.getH(),
                    target_rotation,
                    MOVEMENT.ENEMY_MAX_TURN_SPEED_DEGREES * dt,
                )
            )

        self.model.setX(self.model.getX() - x_direction)
        self.model.setY(self.model.getY() - y_direction)

    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()
