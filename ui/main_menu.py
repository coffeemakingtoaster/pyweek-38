from ui.ui_base import ui_base 
from constants.events import EVENT_NAMES
from helpers.config import save_config
from panda3d.core import TextNode, TransparencyAttrib

from direct.gui.DirectGui import DirectButton, DirectLabel, DirectFrame, DGG

import sys

class main_menu(ui_base):
    def __init__(self):
        ui_base.__init__(self)

        TEXT_COLOR = (0.82, 0.34, 0.14, 1) #  NEW: rgb(208, 86, 36) (0.82f, 0.34f, 0.14f, 1f)
        TEXT_ALTERNATE_COLOR = (1.0, 0.84, 0.62, 1) # rgb(255, 214, 159) (1f, 0.84f, 0.62f, 1f)
        
        #buttonImages = (
        #    loader.loadTexture("assets/textures/button_bg.png"),
        #    loader.loadTexture("assets/textures/button_bg.png"),
        #    loader.loadTexture("assets/textures/button_bg.png"),
        #    loader.loadTexture("assets/textures/button_bg.png")
        #)

        buttonImages = loader.loadTexture("assets/textures/button_bg.png"),

        
        self.ui_elements = []
        self.menu_elements = []

        self.font = loader.loadFont("assets/fonts/NewAmsterdam-Regular.ttf")
        
        self.load_background_image()

        game_logo = DirectFrame(
            frameSize=(-0.5, 0.5, -0.23, 0.23),
            frameColor = (1,1,1,1),
            pos=(-0.84,0,0.60),
            frameTexture = "assets/textures/game_logo_bright.png"
        )
        game_logo.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(game_logo)

        menu_box = DirectFrame( 
            frameSize=(-0.60, 0.60, -0.80, 0.30),
            pos=(-0.85, 0, 0), 
            frameColor = (1,1,1,1),
            frameTexture = "assets/textures/main_menu_board.png"
        )
        menu_box.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(menu_box)
        
        start_button = DirectButton(text=("Start"),
                    parent = menu_box,
                    pos=(0,0,0.05), 
                    scale=0.12, 
                    command=self.start_game, 
                    relief=DGG.FLAT, 
                    text_fg=(TEXT_COLOR),
                    text_font = self.font, 
                    #text_align = TextNode.ACenter, 
                    frameTexture = buttonImages,
                    #pad = (1, 0.1),
                    frameSize = (-4, 4, -1, 1),
                    text_scale = 1.3,
                    text_pos = (0, -0.3),
                    frameColor = (1,1,1,1))
        start_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(start_button)

        settings_button = DirectButton(text=("Settings"),
                    parent = menu_box,
                    pos=(0,0,-0.25), 
                    scale=0.12, 
                    command=self.open_settings, 
                    relief=DGG.FLAT, 
                    text_fg=(TEXT_COLOR),
                    text_font = self.font, 
                    #text_align = TextNode.ACenter, 
                    frameTexture = buttonImages,
                    #pad = (1, 0.1),
                    frameSize = (-4, 4, -1, 1),
                    text_scale = 1.3,
                    text_pos = (0, -0.3),
                    frameColor = (1,1,1,1))
        settings_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(settings_button)

        quit_button = DirectButton(text=("Quit"),
                    parent = menu_box,
                    pos=(0,0,-0.55), 
                    scale=0.12, 
                    command=self.quit_game, 
                    relief=DGG.FLAT, 
                    text_fg=(TEXT_COLOR),
                    text_font = self.font, 
                    #text_align = TextNode.ACenter, 
                    frameTexture = buttonImages,
                    #pad = (1, 0.1),
                    frameSize = (-4, 4, -1, 1),
                    text_scale = 1.3,
                    text_pos = (0, -0.3),
                    frameColor = (1,1,1,1))
        quit_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(quit_button)

        self.ui_elements += self.menu_elements
        
    def start_game(self):
        print("Start button pressed")
        # Use global event messenger to start the game
        messenger.send(EVENT_NAMES.START_GAME) 

    def open_settings(self):
        messenger.send(EVENT_NAMES.GOTO_SETTINGS_MENU)
        
    def quit_game(self):
        save_config('./user_settings.json')
        sys.exit()
