import math

from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point2, CollisionNode, CollisionBox, Point3, CollisionHandlerEvent, CollisionEntry

from constants.events import EVENT_NAMES
from constants.layers import VIEW_COLLISION_BITMASK
from entities.entity_base import EntityBase
from constants.enemy_const import MOVEMENT
from handler.station_handler import StationHandler
from helpers.math_helper import get_limited_rotation_target
from helpers.model_helpers import load_particles

import uuid
import random

from helpers.pathfinding_helper import get_path_from_to_tile_type, global_pos_to_grid, grid_pos_to_global
from helpers.recipe_helper import RECIPES, Routine, Step, build_overwrite_routine, get_routine_at_step


class Enemy(EntityBase):
    def __init__(self, spawn_x, spawn_y, station_handler: StationHandler | None, display_waypoint_info=False):
        super().__init__()
        self.id = f"enemy-{str(uuid.uuid4())}"
        self.move_speed = MOVEMENT.ENEMY_MOVEMENT_SPEED

        self.display_waypoint_info = display_waypoint_info
        self.waypoint_displays = []
        self.waypoint_hitboxes = []

        self.model = Actor("assets/models/MapObjects/Enemy1/Enemy1.bam", {"Idle": "assets/models/MapObjects/Oven/Oven.bam"})
        self.model.setPos(spawn_x, spawn_y, MOVEMENT.ENEMY_FIXED_HEIGHT)

        self.model.reparentTo(render)
        self.__spawn_viewcone()
        self.walk_particles = load_particles("dust")
        self.walk_particles_active = False
        self.recipe: str = random.choice(list(RECIPES.keys()))
        self.routine = Routine(key=self.recipe)
        self.waypoints = get_path_from_to_tile_type(global_pos_to_grid(self.model.getPos()),self.routine.current_step.target) 
        self.__show_waypoints()
        self.desired_pos = grid_pos_to_global(self.waypoints.pop(0))
        self.accept(EVENT_NAMES.SNEAKING, self.__hide_viewcone)

        if station_handler is None:
            print("Warning: Initialize station handler before creating enemies")

        self.station_handler = station_handler

    # TODO: Revisit the viewcone/hitbox;
    #  Viewcone is being stashed & not displayed, but still sees player with "{self.id}-into-player_hitbox" event.
    def __hide_viewcone(self, sneak):
        if sneak:
            self.viewcone.unstash()
        elif not sneak:
            self.viewcone.stash()

    def __show_waypoints(self):
        if not self.display_waypoint_info:
            return
        # no cleanup for hitboxes because they are children anyway
        for node in self.waypoint_displays:
            node.removeNode()

        self.waypoint_displays = []

        for pos in self.waypoints:
            node = render.attachNewNode(f"waypoint_marker{pos[0]}{pos[1]}")
            node.setPos(grid_pos_to_global((pos[0],pos[1])))

            hitbox = node.attachNewNode(CollisionNode(f"wp{pos[0]}:{pos[1]}"))
            hitbox.show()
            hitbox.node().addSolid(CollisionBox(Point3(-0.1,-0.1,0), 0.2, 0.2, 0.5))
            hitbox.setCollideMask(0)

            self.waypoint_displays.append(node)
            self.waypoint_hitboxes.append(hitbox)

    def __spawn_viewcone(self):
        # setup hitboxes
        self.viewcone = self.model.attachNewNode(CollisionNode("enemy_viewcone"))
        self.viewcone.setCollideMask(VIEW_COLLISION_BITMASK)

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
        pass
        #print(f"I ({self.id}) see the player")

    def __handle_player_leave_viewcone(self, _: CollisionEntry):
        pass
        #print(f"I ({self.id}) lost him")

    def update(self, dt):
        self.model.node().resetAllPrevTransform()
        current_pos = self.model.getPos()
        delta_to_end = Vec3(current_pos.x - self.desired_pos.x, current_pos.y - self.desired_pos.y,
                            current_pos.z - self.desired_pos.z)
        normalized = Point2(delta_to_end.x, delta_to_end.y).normalized()

        x_direction = normalized.x * self.move_speed * dt
        y_direction = normalized.y * self.move_speed * dt

        # TODO: implement check if error occured

        if delta_to_end.length() <= 0.1:
            x_direction = 0
            y_direction = 0
            if len(self.waypoints) == 0:
                if not self.__interact_with_item_and_get_success():
                    # -1 -> get a new recipe! This one is blocked
                    if self.routine.current_step.onfail_goto_step == -1:
                        self.routine.current_step.next = None
                    else:
                        # goto failover step
                        self.routine.current_step = Step(
                            "tmp",
                            target=None,
                            next=get_routine_at_step(self.recipe, self.routine.current_step.onfail_goto_step)
                        )
                if self.routine.current_step.next is None:
                    print("new recipe!")
                    self.recipe = random.choice(list(RECIPES.keys()))
                    self.routine.get_new_recipe(self.recipe)
                # currently disabled
                elif False:
                    self.routine.insert_immediate_overwrite("example")
                else:
                    self.routine.advance()
                self.waypoints = self.routine.get_waypoints(
                    self.get_central_pos(),
                    self.id
                ) 
                # does this have to go below the grid update again?
                self.target_grid_var = self.waypoints[-1]
                # Is the target a station that only one can use?
                if TARGET_BLOCKING_MAP[self.routine.current_step.target]:
                    print(self.target_grid_var)
                    base.usage_handler.set_cord_status(self.target_grid_var, True, self.id)
            self.__show_waypoints()
            next_pos = grid_pos_to_global(self.waypoints.pop(0)) 
            self.desired_pos = Point3(
                next_pos.x - self.model.getScale().x/2,
                next_pos.y - self.model.getScale().y/2,
                next_pos.z
            )

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

    def __interact_with_item_and_get_success(self):
        station = None
        # are we going to a specific target?
        if (uuid := self.routine.get_step_target_uuid()) is not None:
            print(f"I am at {self.routine.current_step.name} better go to target with uuid {uuid}")
            station = self.station_handler.get_station_by_uuid(uuid)
        else:
            station = self.station_handler.get_closest_station_by_type(self.get_central_pos(), self.routine.current_step.target)
        if station is None: 
            print("Could not find station")
            return False
        station.ai_interact(None, self)
        self.routine.update_memory(station.uuid)
        return True

    def get_central_pos(self):
        return Point3(
            self.model.getPos().x + self.model.getScale().x / 2,
            self.model.getPos().y + self.model.getScale().y / 2,
            self.model.getPos().z
        )

    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()
