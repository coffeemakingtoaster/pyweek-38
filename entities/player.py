from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point3, CollisionNode, CollisionSphere

import math

from constants.player_const import MOVEMENT
from entities import station
from entities.dish import Dish
from entities.entity_base import EntityBase
from constants import player_const
from entities.item_base import ItemBase
from helpers.math_helper import get_limited_rotation_target
from helpers.model_helpers import load_particles, load_model


class Player(EntityBase):
    def __init__(self):
        super().__init__()

        self.id = "player"
        self.move_speed = MOVEMENT.PLAYER_MOVEMENT_SPEED
        self.movement_status = {"up": 0, "down": 0, "left": 0, "right": 0}
        self.holding = ItemBase("empty_hands", load_model("empty_plate"))

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
                           {"Idle": "assets/models/MapObjects/Player/Player.bam"})
        self.model.setPos(0, 0, MOVEMENT.PLAYER_FIXED_HEIGHT)
        self.model.reparentTo(render)

        self.walk_particles = load_particles("dust")
        self.walk_particles_active = False
        self.__add_player_collider()

    def __add_player_collider(self):
        self.hitbox = self.model.attachNewNode(CollisionNode("player_hitbox"))
        self.hitbox.show()
        self.hitbox.setPos(0, 0, 0)
        self.hitbox.node().addSolid(CollisionSphere(Point3(0, 0, 0), 1))

    def set_movement_status(self, direction):
        self.movement_status[direction] = 1

    def unset_movement_status(self, direction):
        self.movement_status[direction] = 0

    def set_interact(self):
        # TODO: Find Station
        # station.interact
        self.set_holding(Dish("empty_plate", load_model("empty_plate")))
        print("Interacting.")

    def unset_interact(self):
        print("Disabling interact.")

    def set_holding(self, new_item):
        self.holding.model.removeNode()
        # ep = load_model(new_item.id)
        ep = new_item.model
        ep.reparentTo(self.model)
        ep.setPos(3, 0, 0)
        self.holding = new_item

        # ep = load_model("empty_plate")
        # ep.reparentTo(self.model)
        # ep.setPos(2, 0, 2)

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

        if movement_direction.length() > (
                player_const.MOVEMENT.PLAYER_DUST_PARTICLES_MIN_WALKING_SPEED * dt) and not self.walk_particles_active:
            self.walk_particles = load_particles("dust")
            self.walk_particles.start(self.model, renderParent=render)
            self.walk_particles_active = True

        if movement_direction.length() < (
                player_const.MOVEMENT.PLAYER_DUST_PARTICLES_MIN_WALKING_SPEED * dt) and self.walk_particles_active:
            self.walk_particles.softStop()
            self.walk_particles_active = False

        self.model.setFluidPos(
            self.model.getX() + movement_direction.x,
            self.model.getY() + movement_direction.y,
            player_const.MOVEMENT.PLAYER_FIXED_HEIGHT
        )

    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()
