from ui.ui_base import ui_base 

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
        
        quit_button = DirectButton(text=("Quit"), pos=(0,0,-0.6), scale=0.2, command=self.quit_game, relief=None, text_fg=(0,0,0,1))
        self.ui_elements.append(quit_button)
        
    def start_game(self):
        print("Start button pressed")
        # Use global event messenger to start the game
        messenger.send('start_game') 
        
    def quit_game(self):
        sys.exit()
