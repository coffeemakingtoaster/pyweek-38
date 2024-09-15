from ui.ui_base import ui_base 
from constants.events import EVENT_NAMES
from helpers.config import save_config
from panda3d.core import TextNode, TransparencyAttrib

from direct.gui.DirectGui import DirectButton, DirectLabel, DirectFrame, DGG

import sys

class main_menu(ui_base):
    def __init__(self):
        ui_base.__init__(self)

        TEXT_COLOR = (0.968, 0.929, 0.835, 1) # rgb(247, 237, 213)
        TEXT_ALTERNATE_COLOR = (0.62, 0.67, 0.345, 1) # rgb(158, 172, 88)
        #TEXT_BOX_COLOR = (0.921, 0.776, 0.317, 1) # RGB: 235, 198, 81
        TEXT_BOX_COLOR = (1, 1, 1, 1) # RGB: 235, 198, 81
        
        buttonImages = (
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png")
        )
        
        self.ui_elements = []
        self.menu_elements = []

        self.font = loader.loadFont("assets/fonts/NewAmsterdam-Regular.ttf")
        
        self.load_background_image()

        menu_box = DirectFrame(
            frameColor=TEXT_BOX_COLOR, 
            frameSize=(-0.8, 0.8, 0.8, -0.8),
            pos=(-0.85, 0, 0), 
            frameTexture = "assets/textures/main_menu_board.png"
        )
        menu_box.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(menu_box)
        
        self.menu_elements.append(DirectLabel(
            parent = menu_box,
            text="- Definitely not -", 
            scale=0.1, 
            pos=(0,0,0.55), 
            relief=None, 
            text_fg=(TEXT_COLOR), 
            text_font = self.font, 
            text_align = TextNode.ACenter)
        )

        self.menu_elements.append(DirectLabel(
            parent = menu_box,
            text="Overcooked", 
            scale=0.2, 
            pos=(0,0,0.3), 
            relief=None, 
            text_fg=(TEXT_COLOR), 
            text_font = self.font, 
            text_align = TextNode.ACenter)
        )
        
        start_button = DirectButton(text=("Start"),
                    parent = menu_box,
                    pos=(0,0,0.05), 
                    scale=0.12, 
                    command=self.start_game, 
                    relief=DGG.FLAT, 
                    text_fg=(TEXT_ALTERNATE_COLOR),
                    text_font = self.font, 
                    #text_align = TextNode.ACenter, 
                    frameTexture = buttonImages,
                    #pad = (1, 0.1),
                    frameSize = (-4, 4, -1, 1),
                    text_scale = 1.3,
                    text_pos = (0, -0.3))
        start_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(start_button)

        settings_button = DirectButton(text=("Settings"),
                    parent = menu_box,
                    pos=(0,0,-0.25), 
                    scale=0.12, 
                    command=self.start_game, 
                    relief=DGG.FLAT, 
                    text_fg=(TEXT_ALTERNATE_COLOR),
                    text_font = self.font, 
                    #text_align = TextNode.ACenter, 
                    frameTexture = buttonImages,
                    #pad = (1, 0.1),
                    frameSize = (-4, 4, -1, 1),
                    text_scale = 1.3,
                    text_pos = (0, -0.3))
        settings_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(settings_button)

        quit_button = DirectButton(text=("Quit"),
                    parent = menu_box,
                    pos=(0,0,-0.55), 
                    scale=0.12, 
                    command=self.quit_game, 
                    relief=DGG.FLAT, 
                    text_fg=(TEXT_ALTERNATE_COLOR),
                    text_font = self.font, 
                    #text_align = TextNode.ACenter, 
                    frameTexture = buttonImages,
                    #pad = (1, 0.1),
                    frameSize = (-4, 4, -1, 1),
                    text_scale = 1.3,
                    text_pos = (0, -0.3))
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
