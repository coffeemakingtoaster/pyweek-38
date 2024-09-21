from ui.ui_base import ui_base 
from panda3d.core import TransparencyAttrib, TextNode
from constants.events import EVENT_NAMES

from direct.gui.DirectGui import DirectButton, DirectLabel, DirectDialog, DirectFrame, DGG

class pause_menu(ui_base):
    def __init__(self):
        ui_base.__init__(self)

        TEXT_COLOR = (0.82, 0.34, 0.14, 1) #  NEW: rgb(208, 86, 36) (0.82f, 0.34f, 0.14f, 1f)
        TEXT_ALTERNATE_COLOR = (1.0, 0.84, 0.6, 1) # rgb(255, 214, 159) (1f, 0.84f, 0.62f, 1f)
        TEXT_BOX_COLOR = (1, 1, 1, 1) # RGB: 235, 198, 81

        buttonImages = (
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png")
        )

        controls_button_image = loader.loadTexture("assets/textures/controls_button.png")
        dishes_button_image = loader.loadTexture("assets/textures/dishes_button.png")

        self.font = loader.loadFont("assets/fonts/NewAmsterdam-Regular.ttf")

        self.ui_elements = []
        self.menu_elements = []

        self.controls_tutorial = DirectDialog(frameSize = (-1.2, 1.2, -0.7, 0.7),
                                   fadeScreen = 0.4,
                                   relief = DGG.FLAT,
                                   frameColor = (1,1,1,1),
                                   frameTexture = "assets/textures/controls_tutorial.png")
        self.controls_tutorial.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(self.controls_tutorial)
        self.controls_tutorial.hide()

        self.dishes_tutorial = DirectDialog(frameSize = (-1.2, 1.2, -0.7, 0.7),
                                   fadeScreen = 0.4,
                                   relief = DGG.FLAT,
                                   frameColor = (1,1,1,1),
                                   frameTexture = "assets/textures/dishes_tutorial.png")
        self.dishes_tutorial.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(self.dishes_tutorial)
        self.dishes_tutorial.hide()

        controls_button = DirectButton(
            pos=(-1.2,0,0.8), 
            scale=0.12, 
            command=self.controls_tutorial.show, 
            relief=DGG.FLAT, 
            text_fg=(TEXT_COLOR),
            text_font = self.font,
            frameColor = (1,1,1,1), 
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
            command=self.dishes_tutorial.show, 
            relief=DGG.FLAT, 
            text_fg=(TEXT_COLOR),
            frameColor = (1,1,1,1),
            text_font = self.font, 
            #text_align = TextNode.ACenter, 
            frameTexture = dishes_button_image,
            #pad = (1, 0.1),
            frameSize = (-1, 1, -1, 1),
        )
        dishes_button.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(dishes_button)

        menu_box = DirectFrame(
            frameSize=(-0.7, 0.7, 0.7, -0.7),
            pos=(0, 0, 0),
            frameColor = (1,1,1,1), 
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
            text_fg=(TEXT_ALTERNATE_COLOR), 
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
                    text_pos = (0, -0.2),
                    frameColor = (1,1,1,1))
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
                    text_pos = (0, -0.2),
                    frameColor = (1,1,1,1))
        settings_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(settings_button)

    def unpause_game(self):
        messenger.send(EVENT_NAMES.PAUSE_GAME) 
    
    def goto_main_menu(self):
        messenger.send(EVENT_NAMES.GOTO_MAIN_MENU) 
