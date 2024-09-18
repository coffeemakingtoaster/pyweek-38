from abc import ABC

from panda3d.core import Vec3

from entities.entity_base import EntityBase


class CameraMovement(EntityBase, ABC):
    def __init__(self, player_model, camera):
        super().__init__()
        self.player_model = player_model
        self.camera = camera
        self.s = None

        self.camera.setHpr(0, -45, 0)

    def setup(self):
        self.camera.lookAt(self.player_model.getPos())

    def update(self, dt):
        self.player_model.node().resetAllPrevTransform()

        self.s = Vec3(((self.player_model.getX() - self.camera.getX()) * 2 * dt),
                      (((self.player_model.getY() - 8) - self.camera.getY()) * 2 * dt)
                      , 0)

        self.camera.setFluidPos(
            self.camera.getX() + self.s.x,
            self.camera.getY() + self.s.y,
            8
        )
