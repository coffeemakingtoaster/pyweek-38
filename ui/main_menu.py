from ui.ui_base import ui_base 
from constants.events import EVENT_NAMES

from direct.gui.DirectGui import DirectButton, DirectLabel

import sys

class main_menu(ui_base):
    def __init__(self):
        ui_base.__init__(self)
        
        self.ui_elements = []
        
        self.load_background_image()
        
        self.ui_elements.append(DirectLabel(text="Sample text", scale=0.25, pos=(0,0,0.5), relief=None, text_fg=(0,0,0,1)))
        
        start_button = DirectButton(text=("Start"),pos=(0,0,0), scale=0.2, command=self.start_game, relief=None, text_fg=(0,0,0,1))
        self.ui_elements.append(start_button)

        settings_button = DirectButton(text=("Settings"),pos=(0,0,-0.3), scale=0.2, command=self.open_settings, relief=None, text_fg=(0,0,0,1))
        self.ui_elements.append(settings_button)
        
        quit_button = DirectButton(text=("Quit"), pos=(0,0,-0.6), scale=0.2, command=self.quit_game, relief=None, text_fg=(0,0,0,1))
        self.ui_elements.append(quit_button)
        
    def start_game(self):
        print("Start button pressed")
        # Use global event messenger to start the game
        messenger.send(EVENT_NAMES.START_GAME) 

    def open_settings(self):
        messenger.send(EVENT_NAMES.GOTO_SETTINGS_MENU)
        
    def quit_game(self):
        sys.exit()
