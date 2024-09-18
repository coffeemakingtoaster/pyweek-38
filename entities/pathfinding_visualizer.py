import math

from direct.actor.Actor import Actor
from direct.showbase.Loader import DirectObject
from panda3d.core import Vec3, Point2, CollisionNode, CollisionBox, Point3, CollisionHandlerEvent, CollisionEntry

from constants.map import PATHFINDING_MAP

from helpers.pathfinding_helper import grid_pos_to_global


class PathfinderVisualizer(DirectObject):
    def __init__(self):
        super().__init__()

        self.parent = render.attachNewNode("visualizer")
        self.parent.setPos(0,0,0)

        self.nodes = []
        self.hitboxes = []

        TILE_SIZE_X = abs(grid_pos_to_global((0,0))[0] - grid_pos_to_global((0,1))[0]) - 0.2
        TILE_SIZE_Y = abs(grid_pos_to_global((0,0))[1] - grid_pos_to_global((1,0))[1]) - 0.2

        for i in range(len(PATHFINDING_MAP)):
            for j in range(len(PATHFINDING_MAP[0])):

                height = 1
                if PATHFINDING_MAP[i][j] == "#":
                    continue

                node = self.parent.attachNewNode(f"{i};{j}")
                node.setPos(grid_pos_to_global((i,j)))
                # setup hitboxes
                hitbox = node.attachNewNode(CollisionNode(f"hb{i}:{j}"))
                hitbox.show()
                hitbox.node().addSolid(CollisionBox(Point3(0,0,0), TILE_SIZE_X, TILE_SIZE_Y, height))
                self.nodes.append(node)
                self.hitboxes.append(hitbox)



