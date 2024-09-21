from panda3d.core import *

from collections import defaultdict
from direct.showbase.ShowBase import ShowBase

from direct.gui.DirectGui import DirectWaitBar
from panda3d.core import TextNode

from direct.gui.OnscreenText import OnscreenText

from direct.task.Task import Task
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from constants.map import TARGETS
from entities.camera_movement import CameraMovement
from handler.music_handler import MusicHandler
from handler.order_handler import OrderHandler
from handler.station_handler import StationHandler
from handler.usage_handler import UsageHandler
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
from direct.showbase import Audio3DManager

loadPrcFile("./settings.prc")


class main_game(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)
        render.setShaderAuto()
        base.enableParticles()
        base.cTrav = None

        base.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.cam)

        self.camera_movement = None
        self.camera = base.cam
        self.enemy = None
        self.player = None
        self.enemies = []
        self.slight = None
        self.ambientLight = None
        self.map_models = []
        self.map_lights = []
        self.map_stations = []
        self.stations_handler = None
        self.order_handler = None
        self.player_in_sight = False

        self.suspicion_level = 0.0
        self.suspicion_max = 100.0
        self.suspicion_bar = None
        self.sustash = None

        properties = WindowProperties()
        properties.setSize(1280, 720)
        self.win.requestProperties(properties)

        self.game_status = GAME_STATUS.MAIN_MENU

        # Create event handlers for events fired by UI
        self.accept(EVENT_NAMES.START_GAME, self.set_game_status, [GAME_STATUS.STARTING])
        # Create event handlers for events fired by keyboard
        self.accept(EVENT_NAMES.ESCAPE, self.toggle_pause)

        self.accept(EVENT_NAMES.PAUSE_GAME, self.toggle_pause)

        self.accept(f"player_entered_viewcone", self.increase_sus)
        self.accept(f"player_left_viewcone", self.decrease_sus)

        self.accept(EVENT_NAMES.GOTO_MAIN_MENU, self.goto_main_menu)
        self.accept(EVENT_NAMES.GOTO_SETTINGS_MENU, self.goto_settings_menu)
        self.accept(EVENT_NAMES.SNEAKING, self.change_light)
        self.gameTask = base.taskMgr.add(self.game_loop, "gameLoop")

        self.status_display = OnscreenText(text=GAME_STATUS.MAIN_MENU, pos=(0.9, 0.9), scale=0.07, fg=(255, 0, 0, 1))

        base.disableMouse()

        self.active_ui = None
        self.active_hud = None

        self.goto_main_menu()

        self.ambientLight = AmbientLight("ambientLight")
        self.ambientLight.setColor((.5, .5, .5, 1))
        alnp = render.attachNewNode(self.ambientLight)
        render.setLight(alnp)
        # Create a spotlight
        self.slight = Spotlight('slight')
        self.slight.setColor((4, 4, 4, 1))  # Set light color
        self.slight.setShadowCaster(True, 4096 * 4, 4096 * 4)  # Enable shadow casting

        # Create a lens for the spotlight and set its field of view
        lens = PerspectiveLens()
        lens.setFov(120)  # Field of view angle (degree)
        self.slight.setLens(lens)

        # Attach the spotlight to a NodePath
        slnp = self.render.attachNewNode(self.slight)

        # Position and rotate the spotlight
        slnp.setPos(0, 17, 17)  # Position the spotlight
        slnp.setHpr(0, -135, 0)  # Make the spotlight point at the model

        # Attach the spotlight to the scene
        self.render.setLight(slnp)

        # Enable shader generation to receive shadows
        self.render.setShaderAuto()

        base.usage_handler = UsageHandler()

        load_config('./user_settings.json')

        # This still reacts to setting changes
        self.music_handler = MusicHandler()


        display_pathfinding_test()

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
        self.update_suspicion(dt)
        
        
        if self.suspicion_level >= 100:
            return

        return Task.cont

    def setup_game(self):
        self.active_ui.destroy()
        base.cTrav = CollisionTraverser()

        self.load_game()

        self.player = Player(self.map_stations)
        self.camera_movement = CameraMovement(self.player.model, self.camera)

        base.audio3d.attachListener(self.player.model)

        self.order_handler = OrderHandler()
        self.enemies = [
            Enemy(3, 3, station_handler=self.stations_handler),
            Enemy(1, 1, station_handler=self.stations_handler),
            Enemy(4, 2, station_handler=self.stations_handler),
        ]
        self.active_hud = hud()

        self.suspicion_bar = DirectWaitBar(
            value=self.suspicion_level,
            pos=(0, 0, 0.86), scale=(0.12, 1, 0.50),
            range=self.suspicion_max,
            barColor=(1, 0, 0, 1),
            text_align=TextNode.ACenter,
            frameColor=(0, 0, 0, 0),
            sortOrder=0
        )

        self.sustash = OnscreenImage(image='mustache_hole.png', pos=(0, 0, 0.85))
        self.sustash.setTransparency(TransparencyAttrib.MAlpha)
        self.sustash.setScale(0.3, 0.6, 0.2)
        self.sustash.setBin('gui-popup', 0)

        # DO NOT DELETE please uwu 
        # show pathfinding grid
        # self.visualizer = PathfinderVisualizer()

    def load_game(self):
        with open('./map.json', 'r') as file:
            data = json.load(file)

        self.map_models, self.map_lights, self.map_stations = load_map(data)
        self.stations_handler = StationHandler(self.map_stations)
        base.usage_handler.set_station_handler(self.stations_handler)

    def set_game_status(self, status):
        self.status_display["text"] = status
        self.game_status = status

    def goto_main_menu(self):
        if self.active_ui is not None:
            self.active_ui.destroy()
        if self.active_hud is not None:
            self.active_hud.destroy()
            self.active_hud = None

        if self.order_handler is not None:
            self.order_handler.destroy()
            self.order_handler = None

        if base.cTrav is not None:
            base.cTrav.clearColliders()
    
        # disable and replace
        base.audio3d.disable()
        base.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.cam)

        if self.suspicion_bar is not None:
            self.suspicion_bar.removeNode()
            
        if self.sustash is not None:
            self.sustash.destroy()
        
        
        if self.player is not None:
            self.player.destroy()

        if len(self.enemies) != 0:
            for i in self.enemies:
                i.destroy()
            self.enemies = []
        self.active_ui = main_menu()

        for model in self.map_models:
            model.removeNode()
        for light in self.map_lights:
            try:
                render.clearLight(light)
                light.removeNode()
            except:
                # There was a bug where this could crash the game
                # I didnt bother fixing it...this will do for now
                pass
        for station in self.map_stations:
            station.destroy()

        # self.setBackgroundColor((0, 0, 0, 1))
        self.set_game_status(GAME_STATUS.MAIN_MENU)

        print(len(render.getChildren()))

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

    def change_light(self, sneak):
        if sneak:
            self.slight.setColor((25, 3, 3, 1))  # Set Red
            self.ambientLight.setColor((0.7, 0, 0, 2))

        elif not sneak:
            self.slight.setColor((4, 4, 4, 1))  # Set Normal
            self.ambientLight.setColor((.5, .5, .5, 1))

    def increase_sus(self):
        self.player_in_sight = True

    def decrease_sus(self):
        self.player_in_sight = False

    def update_suspicion(self, dt):
        if self.player_in_sight and self.player.is_evil:
            self.suspicion_level = min(self.suspicion_level + 40 * dt, self.suspicion_max)
        else:
            self.suspicion_level = max(self.suspicion_level - 1 * dt, 0)

        self.suspicion_bar['value'] = self.suspicion_level


def start_game():
    print("Starting game..")
    game = main_game()
    game.run()


def display_pathfinding_test():
    print(get_path_from_to_tile_type((9, 8), TARGETS.TOMATO_STATION, debug_print=True))


if __name__ == "__main__":
    start_game()
