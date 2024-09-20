from ui.ui_base import ui_base 
from panda3d.core import TransparencyAttrib, TextNode
from constants.events import EVENT_NAMES

from direct.gui.DirectGui import DirectButton, DirectLabel, DirectDialog, DirectFrame, DGG

class pause_menu(ui_base):
    def __init__(self):
        ui_base.__init__(self)

        TEXT_COLOR = (0.968, 0.929, 0.835, 1) # rgb(247, 237, 213)
        TEXT_ALTERNATE_COLOR = (0.62, 0.67, 0.345, 1) # rgb(158, 172, 88)
        TEXT_BOX_COLOR = (1, 1, 1, 1) # RGB: 235, 198, 81

        buttonImages = (
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png")
        )

        controls_button_image = loader.loadTexture("assets/textures/controls_button.png")
        close_button_image = loader.loadTexture("assets/textures/close_button.png")

        self.font = loader.loadFont("assets/fonts/NewAmsterdam-Regular.ttf")

        self.ui_elements = []
        self.menu_elements = []

        self.controls_tutorial = DirectDialog(frameSize = (-1.2, 1.2, -0.7, 0.7),
                                   fadeScreen = 0.4,
                                   relief = DGG.FLAT,
                                   frameTexture = "assets/textures/controls_tutorial.png")
        self.controls_tutorial.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(self.controls_tutorial)
        self.controls_tutorial.hide()

        controls_close_button = DirectButton(
            pos=(-0.5,0,0.8), 
            scale=0.12, 
            command=self.controls_tutorial.hide, 
            relief=DGG.FLAT, 
            frameTexture = close_button_image,
            frameSize = (-1, 1, -1, 1),
        )
        controls_close_button.setTransparency(TransparencyAttrib.MAlpha)
        controls_close_button.hide()
        self.ui_elements.append(controls_close_button)

        controls_button = DirectButton(
            pos=(-1.2,0,0.8), 
            scale=0.12, 
            command=self.controls_tutorial.show, 
            relief=DGG.FLAT, 
            text_fg=(TEXT_COLOR),
            text_font = self.font, 
            #text_align = TextNode.ACenter, 
            frameTexture = controls_button_image,
            #pad = (1, 0.1),
            frameSize = (-1, 1, -1, 1),
        )
        controls_button.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(controls_button)

        

        dishes_button = DirectButton(
            pos=(-1.5,0,0.8), 
            scale=0.12, 
            command=self.unpause_game, 
            relief=DGG.FLAT, 
            text_fg=(TEXT_COLOR),
            text_font = self.font, 
            #text_align = TextNode.ACenter, 
            frameTexture = controls_button_image,
            #pad = (1, 0.1),
            frameSize = (-1, 1, -1, 1),
        )
        dishes_button.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(dishes_button)

        menu_box = DirectFrame(
            frameColor=TEXT_BOX_COLOR, 
            frameSize=(-0.7, 0.7, 0.7, -0.7),
            pos=(0, 0, 0), 
            frameTexture = "assets/textures/main_menu_board.png"
        )
        menu_box.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(menu_box)

        self.menu_elements.append(DirectLabel(
            parent = menu_box,
            text="PAUSE", 
            scale=0.2, 
            pos=(0,0,0.4), 
            relief=None, 
            text_fg=(TEXT_COLOR), 
            text_font = self.font, 
            text_align = TextNode.ACenter)
        )
        
        start_button = DirectButton(text=("Continue"),
                    parent = menu_box,
                    pos=(0,0,0.05), 
                    scale=0.15, 
                    command=self.unpause_game, 
                    relief=DGG.FLAT, 
                    text_fg=(TEXT_COLOR),
                    text_font = self.font, 
                    #text_align = TextNode.ACenter, 
                    frameTexture = buttonImages,
                    #pad = (1, 0.1),
                    frameSize = (-4, 4, -1, 1),
                    text_scale = 1.0,
                    text_pos = (0, -0.2))
        start_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(start_button)

        settings_button = DirectButton(text=("Return to main menu"),
                    parent = menu_box,
                    pos=(0,0,-0.35), 
                    scale=0.15, 
                    command=self.goto_main_menu, 
                    relief=DGG.FLAT, 
                    text_fg=(TEXT_COLOR),
                    text_font = self.font, 
                    #text_align = TextNode.ACenter, 
                    frameTexture = buttonImages,
                    #pad = (1, 0.1),
                    frameSize = (-4, 4, -1, 1),
                    text_scale = 1.0,
                    text_pos = (0, -0.2))
        settings_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(settings_button)

    def unpause_game(self):
        messenger.send(EVENT_NAMES.PAUSE_GAME) 
    
    def goto_main_menu(self):
        messenger.send(EVENT_NAMES.GOTO_MAIN_MENU) 
