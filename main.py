from panda3d.core import *

from direct.showbase.ShowBase import ShowBase

from direct.gui.OnscreenText import OnscreenText

from direct.task.Task import Task

from helpers.config import load_config
from ui.hud import hud
from ui.main_menu import main_menu
from ui.pause_menu import pause_menu

from constants.game_state import GAME_STATUS
from constants.events import EVENT_NAMES 

from helpers.game_helpers import  release_mouse_from_window, lock_mouse_in_window
from helpers.model_helpers import load_model
from ui.settings_menu import settings_menu

from entities.player import Player
from entities.enemy import Enemy

loadPrcFile("./settings.prc")

class main_game(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)
        render.setShaderAuto()
        base.enableParticles()
        
        self.enemy = None
        self.player = None
        self.enemies = []
        
        # random coords
        base.cam.setPos(0, 0, 40)
        # Assumption: Player is spawned at 0,0,0
        # Simplest way to ensure we look at the player is by using quaterions
        # This allows us to move the camera without having to recalculate the hpr ourselves :)
        quat = Quat()
        lookAt(quat, Point3(0,0,0) - base.cam.getPos(), Vec3.up())
        base.cam.setQuat(quat)
       
        self.game_status = GAME_STATUS.MAIN_MENU

        # Create event handlers for events fired by UI
        self.accept(EVENT_NAMES.START_GAME, self.set_game_status, [GAME_STATUS.STARTING])

        # Create event handlers for events fired by keyboard
        self.accept(EVENT_NAMES.ESCAPE, self.toggle_pause)

        self.accept(EVENT_NAMES.PAUSE_GAME, self.toggle_pause)
        
        self.accept(EVENT_NAMES.GOTO_MAIN_MENU, self.goto_main_menu)
        self.accept(EVENT_NAMES.GOTO_SETTINGS_MENU, self.goto_settings_menu)

        self.gameTask = base.taskMgr.add(self.game_loop, "gameLoop")

        self.status_display = OnscreenText(text=GAME_STATUS.MAIN_MENU, pos=(0.9,0.9 ), scale=0.07,fg=(255,0,0, 1))
        
        base.disableMouse()

        self.active_ui = None 
        self.active_hud = None
        
        self.goto_main_menu()
        
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((5, 5, 5, 5))
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

        return Task.cont

    def setup_game(self):
        self.active_ui.destroy()

        self.player = Player()
        self.enemies = [Enemy(3, 3)]
        self.active_hud = hud()
        # TODO: this would be the place to setup the game staff and initialize the ui uwu
        
    def set_game_status(self, status):
        self.status_display["text"] = status
        self.game_status = status

    def goto_main_menu(self):
        if self.active_ui is not None:
            self.active_ui.destroy()
        if self.active_hud is not None:
            self.active_hud.destroy()
            self.active_hud = None

        if self.player is not None:
            self.player.destroy()

        if len(self.enemies) != 0:
            for i in self.enemies:
                i.destroy()
            self.enemies = []

        self.active_ui = main_menu()
        #self.setBackgroundColor((0, 0, 0, 1))
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

if __name__ == "__main__":
    start_game()
