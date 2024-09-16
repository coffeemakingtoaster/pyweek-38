import math

from direct.actor.Actor import Actor
from panda3d.core import CollisionNode, Vec3, Point2, CollisionBox, Point3

from entities.entity_base import EntityBase
from constants.enemy_const import MOVEMENT
from helpers.model_helpers import load_particles


class Enemy(EntityBase):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.id = "enemy"
        self.move_speed = MOVEMENT.ENEMY_MOVEMENT_SPEED

        self.model = Actor("assets/models/Oven/Oven.bam", {"Idle": "assets/models/Oven/Oven.bam"})
        self.model.setPos(spawn_x, spawn_y, MOVEMENT.ENEMY_FIXED_HEIGHT)

        self.model.reparentTo(render)

        # self.spawn_viewcone()
        self.walk_particles = load_particles("dust")
        self.walk_particles_active = False

    # def spawn_viewcone(self):
    #     self.viewcone = self.model.attachNewNode(CollisionNode("Enemy(collider) sees player"))
    #     self.viewcone.show()
    #     self.viewcone.setPos(0, 0, 0)
    #     self.viewcone.node().addSolid(CollisionBox(Point3(0, 0, 0), 2, 3, 1.5))

    def update(self, dt):
        self.model.node().resetAllPrevTransform()
        current_pos = self.model.getPos()
        desired_pos = Vec3(10, 5, MOVEMENT.ENEMY_FIXED_HEIGHT)
        delta_to_end = Vec3(current_pos.x - desired_pos.x, current_pos.y - desired_pos.y, 2)
        normalized = Point2(delta_to_end.x, delta_to_end.y).normalized()

        x_direction = normalized[0] * self.move_speed * dt
        y_direction = normalized[1] * self.move_speed * dt

        print(delta_to_end.length())
        if delta_to_end.length() <= 3:
            print("Reached")
            x_direction = 0
            y_direction = 0

        self.model.setX(self.model.getX() - x_direction)
        self.model.setY(self.model.getY() - y_direction)

    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()
