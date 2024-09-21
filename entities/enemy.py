import math
from panda3d.core import TransparencyAttrib
from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point2, CollisionNode, CollisionBox, Point3, CollisionHandlerEvent, CollisionEntry

from constants.events import EVENT_NAMES
from constants.layers import VIEW_COLLISION_BITMASK
from constants.map import TARGET_BLOCKING_MAP, TARGETS
from entities.ItemArea import ItemArea
from entities.entity_base import EntityBase
from constants.enemy_const import MOVEMENT
from handler.station_handler import StationHandler
from helpers.dish_helper import VIABLE_FINISHED_ORDER_DISHES
from helpers.math_helper import get_limited_rotation_target
from helpers.model_helpers import load_3d_sounds, load_particles
from entities.item_base import ItemBase
from helpers.model_helpers import load_model
from entities.dish import Dish
from entities.CuttingBoard import CuttingBoard

import uuid
import random

from helpers.pathfinding_helper import global_pos_to_grid, grid_pos_to_global, pos_to_string
from helpers.recipe_helper import RECIPES, Routine, Step, get_routine_at_step
from helpers.review_generator import Review


class Enemy(EntityBase):
    def __init__(self, spawn_x, spawn_y, station_handler: StationHandler | None, display_waypoint_info=False):
        super().__init__()
        self.id = f"enemy-{str(uuid.uuid4())}"
        self.move_speed = MOVEMENT.ENEMY_MOVEMENT_SPEED

        self.sneaking = False
        self.viewconeModel = None

        self.display_waypoint_info = display_waypoint_info
        self.waypoint_displays = []
        self.waypoint_hitboxes = []
        self.is_cutting_remaining_duration = None
        
        self.angermodel = None
        self.angertask = None

        enemy = random.randrange(1,4)

        self.model = Actor(f"assets/models/MapObjects/Enemy{enemy}/Enemy{enemy}.bam")
        self.model.setPos(spawn_x, spawn_y, MOVEMENT.ENEMY_FIXED_HEIGHT)

        self.model.reparentTo(render)
        self.__spawn_viewcone()
        # Disable viewcone at beginning of the game
        self.__hide_viewcone(False)
        self.walk_particles = load_particles("dust")
        self.walk_particles_active = False
        #self.recipe: str = random.choice(list(RECIPES.keys()))
        self.recipe = VIABLE_FINISHED_ORDER_DISHES.PIZZA
        self.routine = Routine(key=self.recipe)
        self.waypoints = self.routine.get_waypoints(
            self.model.getPos(), 
            self.id
        ) 
        self.__show_waypoints()
        self.target_grid_var = self.waypoints[-1]
        self.desired_pos = grid_pos_to_global(self.waypoints.pop(0))
        self.accept(EVENT_NAMES.SNEAKING, self.__hide_viewcone)

        if station_handler is None:
            print("Warning: Initialize station handler before creating enemies")

        self.station_handler = station_handler

        self.accept(EVENT_NAMES.RECALCULATE_WAYPOINTS, self.__double_check_waypoints)
        
        self.holding = ItemBase("empty_hands", load_model("empty_hands"))
        self.holding.model.setPos(0, -0.4, 0.76)
        self.holding.model.reparentTo(self.model)

        self.is_recovering = False

        self.sounds = load_3d_sounds("angry",self.model)
        self.accept(EVENT_NAMES.DISPLAY_REVIEW, self.__angry)

    def __angry(self, review: Review):
        if len(self.sounds):
            return
        if review.star_count > 2.5:
            return
        random.choice(self.sounds).play()
        
    # TODO: Revisit the viewcone/hitbox;
    #  Viewcone is being stashed & not displayed, but still sees player with "{self.id}-into-player_hitbox" event.
    def __hide_viewcone(self, sneak):
        if sneak:
            self.grr()
            self.viewcone.unstash()
            self.viewconeModel = load_model("viewcone")
            self.viewconeModel.reparentTo(self.model)
            self.viewconeModel.setPos(0,-1,1)
            self.viewconeModel.setTransparency(TransparencyAttrib.MAlpha)
            self.model.setColor(1, 1, 1, 0.5)
            self.accept(f"{self.id}-into-player_hitbox", self.__handle_player_enter_viewcone)
            self.accept(f"{self.id}-out-player_hitbox", self.__handle_player_leave_viewcone)
        elif not sneak:
            self.viewconeModel.removeNode()
            self.viewcone.stash()
            self.ignore(f"{self.id}-into-player_hitbox")
            self.ignore(f"{self.id}-out-player_hitbox")

    def __double_check_waypoints(self, cords):
        if cords != self.target_grid_var:
            return
        # Recalculate route
        self.waypoints = self.routine.get_waypoints(
            self.get_central_pos(),
            self.id
        ) 
        # does this have to go below the grid update again?
        self.target_grid_var = self.waypoints[-1]
        # Is the target a station that only one can use?
        if TARGET_BLOCKING_MAP[self.routine.current_step.target]:
            base.usage_handler.set_cord_status(self.target_grid_var, True, self.id)
        self.__show_waypoints()
        next_pos = grid_pos_to_global(self.waypoints.pop(0)) 
        self.desired_pos = Point3(
            next_pos.x - self.model.getScale().x/2,
            next_pos.y - self.model.getScale().y/2,
            next_pos.z
        )

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
        self.viewconeModel = load_model("viewcone")
        self.viewconeModel.reparentTo(self.model)
        self.viewconeModel.setPos(0,-1,1)
        self.viewcone.setPos(0, 0, 0)
        self.viewcone.node().addSolid(CollisionBox(Point3(0, -0.6, 0.5), 0.25, -0.75, 0.25))
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
        messenger.send(f"player_entered_viewcone")

    def __handle_player_leave_viewcone(self, _: CollisionEntry):
        print(f"I ({self.id}) lost him")
        messenger.send(f"player_left_viewcone")

    def update(self, dt):
        self.model.node().resetAllPrevTransform()

        if self.is_cutting_remaining_duration is not None:
            self.is_cutting_remaining_duration -= dt
            if self.is_cutting_remaining_duration <= 0:
                self.is_cutting_remaining_duration = None
            else:
                return

        current_pos = self.get_central_pos()
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
                    if self.routine.current_step.repeats > 0:
                        self.is_cutting_remaining_duration = 1
                        return
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
                    if self.holding.id != "empty_hands":
                        self.holding.model.removeNode()
                        self.set_holding(ItemBase("empty_hands", load_model("empty_hands")))

                    self.recipe = random.choice(list(RECIPES.keys()))
                    self.routine.get_new_recipe(self.recipe)
                # currently disabled
                elif False:
                    self.routine.insert_immediate_overwrite("example")
                else:
                    self.routine.advance()
                    print(f"Now at step {self.routine.current_step.name}")
                self.waypoints = self.routine.get_waypoints(
                    self.get_central_pos(),
                    self.id
                ) 
                # pathfinding has failed silently! recover somehow
                if len(self.waypoints) == 1 and self.waypoints[0] == (1,1):
                    self.routine.recover()
                    self.is_recovering = True
                # does this have to go below the grid update again?
                self.target_grid_var = self.waypoints[-1]
                # Is the target a station that only one can use?
                if TARGET_BLOCKING_MAP[self.routine.current_step.target]:
                    base.usage_handler.set_cord_status(self.target_grid_var, True, self.id)
            self.__show_waypoints()
            next_pos = grid_pos_to_global(self.waypoints.pop(0)) 
            self.desired_pos = Point3(
                next_pos.x,
                next_pos.y,
                next_pos.z
            )

        if delta_to_end.length() > 0:
            target_rotation = math.degrees(math.atan2(delta_to_end.x, -delta_to_end.y)) 
            self.model.setH(
                get_limited_rotation_target(
                    self.model.getH(),
                    target_rotation + 180,
                    MOVEMENT.ENEMY_MAX_TURN_SPEED_DEGREES * dt,
                )
            )

        self.model.setX(self.model.getX() - x_direction)
        self.model.setY(self.model.getY() - y_direction)

    def __interact_with_item_and_get_success(self):
        if self.is_recovering:
            self.is_recovering = False
            return True
        station = None
        self.routine.current_step.repeats -= 1
        # are we going to a specific target?
        if (uuid := self.routine.get_step_target_uuid()) is not None:
            station = self.station_handler.get_station_by_uuid(uuid[0])
        else:
            station = self.station_handler.get_closest_station_by_type(self.get_central_pos(), self.routine.current_step.target)
        if station is None: 
            print("Could not find station")
            return False
        if type(station) == CuttingBoard:
            station.ai_interact(self.holding,self)
            if self.holding.id == "empty_hands":
                station.ai_interact(self.holding,self)
                if station.is_cutting:
                    self.is_cutting_remaining_duration = station.duration + 0.25
        elif type(station) == ItemArea:
            # This area should be full...but it is not :/
            if self.routine.current_step.target_from_step is not None and station.inventory.id == "empty_hands":
                if (plate_uuid:=self.routine.remember_my_plate()) is not None:
                    if (station:=self.station_handler.get_station_by_content_uuid(plate_uuid)) is not None:
                        print("lets get it back!")
                        self.routine.item_fetch_interrupt(station.uuid, global_pos_to_grid(station.model.getPos()))
                        print(self.routine.current_step.next.name)
                        return True 
                # plate was lost
                self.routine.current_step.onfail_goto_step = 0
                self.routine.current_step.repeats = 0
                self.set_holding(ItemBase("empty_hands", load_model("empty_hands")))
                return False
            else:
                if self.routine.current_step.target == TARGETS.COUNTERTOP and self.routine.current_step.remember_target:
                    print(self.holding.uuid)
                    self.routine.own_plate(self.holding.uuid)
                station.ai_interact(self.holding, self)
        else:
            # Is the station not done yet
            if station.task is not None:
                return False
            station.ai_interact(self.holding, self)
        if self.routine.current_step.release_target_after:
            base.usage_handler.set_cord_status(self.target_grid_var, False, None, station.uuid)
        self.routine.update_memory(station.uuid, global_pos_to_grid(self.get_central_pos()))
        return True

    def get_central_pos(self):
        return Point3(
            self.model.getPos().x,
            self.model.getPos().y,
            self.model.getPos().z
        )

    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()
        for sound in self.sounds:
            sound.stop()

    def set_holding(self, new_item):
        if type(self.holding) == Dish and new_item.id is not "empty_hands" and type(new_item) is not Dish:
            if self.holding.add_ingredient(new_item.id):
                self.holding.model.reparentTo(self.model)
                return True
            else:
                return False
        else:
            self.hardset(new_item)

    def hardset(self, item):
        self.holding.model.removeNode()

        ep = item.model
        ep.reparentTo(self.model)

        ep.setPos(0, -0.5, 0.76)
        self.holding = item

    def grr(self):
        if self.angertask:
            self.its_ok("task")
        self.angertask = taskMgr.doMethodLater(2,self.its_ok,"task")
        self.angermodel = load_model("Anger")
        self.angermodel.reparentTo(self.model)
        self.angermodel.setPos(0,0,1.5)
        self.angermodel.setScale(2)
        
    def its_ok(self,name):
        if self.angermodel:
            self.angermodel.removeNode()
        self.angermodel = None
        
