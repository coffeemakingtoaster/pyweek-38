from panda3d.core import *

from direct.showbase.ShowBase import ShowBase

from direct.gui.OnscreenText import OnscreenText

from direct.task.Task import Task

from entities.camera_movement import CameraMovement
from entities.pathfinding_visualizer import PathfinderVisualizer
from helpers.config import load_config
from helpers.pathfinding_helper import get_path_from_to_tile_type
from ui.hud import hud
from ui.main_menu import main_menu
from ui.pause_menu import pause_menu
from constants.game_state import GAME_STATUS
from constants.events import EVENT_NAMES

from helpers.game_helpers import release_mouse_from_window, lock_mouse_in_window
from entities.map_loader import load_map
from ui.settings_menu import settings_menu

from entities.player import Player
import json
from entities.enemy import Enemy

loadPrcFile("./settings.prc")

class main_game(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)
        render.setShaderAuto()
        base.enableParticles()
        base.cTrav = None

        self.camera_movement = None
        self.camera = base.cam
        self.enemy = None
        self.player = None
        self.enemies = []
        
        self.map_models =[]
        self.map_lights =[]
        self.map_stations =[]

        properties = WindowProperties()
        properties.setSize(1280, 720)
        self.win.requestProperties(properties)

        self.game_status = GAME_STATUS.MAIN_MENU

        # Create event handlers for events fired by UI
        self.accept(EVENT_NAMES.START_GAME, self.set_game_status, [GAME_STATUS.STARTING])

        # Create event handlers for events fired by keyboard
        self.accept(EVENT_NAMES.ESCAPE, self.toggle_pause)

        self.accept(EVENT_NAMES.PAUSE_GAME, self.toggle_pause)

        self.accept(EVENT_NAMES.GOTO_MAIN_MENU, self.goto_main_menu)
        self.accept(EVENT_NAMES.GOTO_SETTINGS_MENU, self.goto_settings_menu)

        self.gameTask = base.taskMgr.add(self.game_loop, "gameLoop")

        self.status_display = OnscreenText(text=GAME_STATUS.MAIN_MENU, pos=(0.9, 0.9), scale=0.07, fg=(255, 0, 0, 1))

        base.disableMouse()

        self.active_ui = None
        self.active_hud = None

        self.goto_main_menu()

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.1, .1, .1, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, -45, -45))
        directionalLight.setColor((2, 2, 2, 1))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(ambientLight))

        load_config('./user_settings.json')

    def game_loop(self, task):
        # Runtime check. DO NOT PUT ANY GAMELOGIC BEFORE THIS
        if self.game_status == GAME_STATUS.STARTING:
            print("Starting")
            self.setup_game()
            self.set_game_status(GAME_STATUS.RUNNING)

        if self.game_status != GAME_STATUS.RUNNING:
            return Task.cont

            # use dt for update functions
        dt = self.clock.dt

        for enemy in self.enemies:
            enemy.update(dt)
        self.player.update(dt)
        self.camera_movement.update(dt)

        return Task.cont

    def setup_game(self):
        self.active_ui.destroy()
        self.load_game()
        
        print(self.map_stations)

        base.cTrav = CollisionTraverser()

        self.player = Player(self.map_stations)
        self.camera_movement = CameraMovement(self.player.model, self.camera)
        
        self.enemies = [Enemy(3, 3), Enemy(3, 3,"B")]
        self.active_hud = hud()
        # show pathfinding grid
        self.visualizer = PathfinderVisualizer()
        # TODO: this would be the place to setup the game stuff and initialize the ui uwu

    def load_game(self):
        with open('./map.json', 'r') as file:
            data = json.load(file)

        self.map_models,self.map_lights,self.map_stations = load_map(data)

    def set_game_status(self, status):
        self.status_display["text"] = status
        self.game_status = status

    def goto_main_menu(self):
        if self.active_ui is not None:
            self.active_ui.destroy()
        if self.active_hud is not None:
            self.active_hud.destroy()
            self.active_hud = None

        if base.cTrav is not None:
           base.cTrav.clearColliders()

        if self.player is not None:
            self.player.destroy()

        if len(self.enemies) != 0:
            for i in self.enemies:
                i.destroy()
            self.enemies = []

        self.active_ui = main_menu()
        # self.setBackgroundColor((0, 0, 0, 1))
        self.set_game_status(GAME_STATUS.MAIN_MENU)

    def goto_settings_menu(self):
        if self.active_ui is not None:
            self.active_ui.destroy()
        self.active_ui = settings_menu()
        self.set_game_status(GAME_STATUS.SETTINGS)

    def toggle_pause(self):
        if self.game_status == GAME_STATUS.RUNNING:
            self.set_game_status(GAME_STATUS.PAUSED)
            release_mouse_from_window()
            self.active_ui = pause_menu()
        elif self.game_status == GAME_STATUS.PAUSED:
            self.active_ui.destroy()
            lock_mouse_in_window()
            self.set_game_status(GAME_STATUS.RUNNING)


def start_game():
    print("Starting game..")
    game = main_game()
    game.run()


def display_pathfinding_test():
    print(get_path_from_to_tile_type((4, 5), 'A', True))


if __name__ == "__main__":
    display_pathfinding_test()
    start_game()
