from ui.ui_base import ui_base
from constants.events import EVENT_NAMES
from panda3d.core import TextNode, TransparencyAttrib

from helpers.config import set_music_volume, set_sfx_volume, set_fullscreen_value, get_music_volume, get_sfx_volume, get_fullscreen_value, get_fps_counter_enabled, set_fps_counter_enabled

from direct.gui.DirectGui import DirectButton, DirectCheckButton, DirectSlider, DirectLabel, DirectFrame, DGG, OnscreenImage

from os.path import join

class settings_menu(ui_base):
    def __init__(self) -> None:
        super().__init__()

        self.load_background_image()

        TEXT_COLOR = (0.82, 0.34, 0.14, 1) #  NEW: rgb(208, 86, 36) (0.82f, 0.34f, 0.14f, 1f)
        TEXT_ALTERNATE_COLOR = (1.0, 0.84, 0.62, 1) # rgb(255, 214, 159) (1f, 0.84f, 0.62f, 1f)
        TEXT_BOX_COLOR = (1, 1, 1, 1) # RGB: 235, 198, 81

        buttonImages = (
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png"),
            loader.loadTexture("assets/textures/button_bg.png")
        )

        self.font = loader.loadFont("assets/fonts/NewAmsterdam-Regular.ttf")

        self.menu_elements = []

        menu_box = DirectFrame(
            frameColor=TEXT_BOX_COLOR, 
            frameSize=(-1.2, 1.2, 0.8, -0.8),
            pos=(0, 0, 0), 
            frameTexture = "assets/textures/main_menu_board.png"
        )
        menu_box.setTransparency(TransparencyAttrib.MAlpha)
        self.ui_elements.append(menu_box)

        self.menu_elements.append(DirectLabel(
            parent = menu_box,
            text="Settings", 
            scale=0.2, 
            pos=(0,0,0.5), 
            relief=None, 
            text_fg=(TEXT_ALTERNATE_COLOR), 
            text_font = self.font, 
            text_align = TextNode.ACenter)
        )

        checkbox_image = loader.loadTexture("assets/textures/checkbox.png")
        checkbox_checked_image = loader.loadTexture("assets/textures/checkbox_checked.png")
        checkmark_image = loader.loadTexture("assets/textures/button_bg.png")                  

        fullscreen_checkbox = DirectCheckButton(
            parent = menu_box,
            text="Fullscreen", 
            pos=(-1,0,0.25),
            scale=0.15, 
            indicatorValue=get_fullscreen_value(), 
            command=self.toggle_fullscreen,
            relief=None,
            boxImage = (checkbox_image, checkbox_checked_image),
            boxPlacement = 'right',
            boxImageScale = 0.5,
            boxRelief = None,
            text_fg=(TEXT_ALTERNATE_COLOR),
            text_font = self.font,
            pad = (0.5,0), 
            text_align = TextNode.ALeft
        )
        fullscreen_checkbox.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(fullscreen_checkbox)

        fps_checkbox = DirectCheckButton(
            parent = menu_box,
            text="Show FPS", 
            pos=(-1,0,0.05),
            scale=0.15,
            relief=None, 
            indicatorValue=get_fps_counter_enabled(), 
            command=self.update_fps,
            boxPlacement = 'right',
            boxRelief = None,
            boxImage = (checkbox_image, checkbox_checked_image),
            boxImageScale = 0.5,
            text_fg=(TEXT_ALTERNATE_COLOR),
            text_font = self.font,
            pad = (1,0), 
            text_align = TextNode.ALeft
        )
        fps_checkbox.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(fps_checkbox)

        current_music_volume = get_music_volume()
        music_slider_text = DirectLabel(
            parent = menu_box,
            text="Music volume",
            relief=None, 
            text_fg=(TEXT_ALTERNATE_COLOR),
            text_font = self.font,
            scale=0.1, 
            pos=(-0.5,0,-0.15)
        )
        self.menu_elements.append(music_slider_text)

        self.music_volume_slider = DirectSlider(
            parent = menu_box,
            pageSize=1, 
            range=(0,100), 
            pos=(-0.5,0,-0.25), 
            value=int(current_music_volume * 100),
            scale=0.06, 
            thumb_image = checkbox_image,
            thumb_scale = 0.2,
            frameSize =  (-3, 3, -0.5, 0.5),
            thumb_relief = None,  
            command=self.update_music_volume,
            geom_scale=(10, 1, 1)
            )
        self.music_volume_slider.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(self.music_volume_slider)

        current_sfx_volume = get_sfx_volume()
        sfx_slider_text = DirectLabel(
            parent = menu_box,
            text="SFX volume",
            text_fg=(TEXT_ALTERNATE_COLOR),
            text_font = self.font,
            relief=None,  
            scale=0.1, 
            pos=(0.5,0,-0.15)
        )
        self.menu_elements.append(sfx_slider_text)

        self.sfx_volume_slider = DirectSlider(
            parent = menu_box,
            pageSize=1, 
            range=(0,100), 
            pos=(0.5,0,-0.25),  
            scale=0.06, 
            thumb_image = checkbox_image,
            frameSize =  (-3, 3, -0.5, 0.5),
            value=int(current_sfx_volume * 100),
            thumb_relief = None,
            command=self.update_sfx_volume)
        self.sfx_volume_slider.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(self.sfx_volume_slider)

        play_sample_sfx_button = DirectButton(
            parent = menu_box,
            text=("Play sample sound"),
            text_fg=(TEXT_COLOR),
            text_font = self.font,
            relief=DGG.FLAT,
            pos=(0.5,0,-0.4), 
            scale=0.05, 
            frameTexture = buttonImages,
            #pad = (1, 0.1),
            frameSize = (-4, 4, -1, 1),
            text_pos = (0, -0.2),
            frameColor = (1,1,1,1),
            command=self.play_sample_sound)
        play_sample_sfx_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(play_sample_sfx_button)

        main_menu_button = DirectButton(
            parent = menu_box,
            text=("Return to main menu"),
            text_fg=(TEXT_COLOR),
            text_font = self.font,
            relief=DGG.FLAT, 
            pos=(0,0,-0.6), 
            scale=0.1, 
            frameTexture = buttonImages,
            #pad = (1, 0.1),
            frameSize = (-4, 4, -1, 1),
            frameColor = (1,1,1,1),
            text_pos = (0, -0.2),
            command=self.return_to_main_menu)
        main_menu_button.setTransparency(TransparencyAttrib.MAlpha)
        self.menu_elements.append(main_menu_button)

    def return_to_main_menu(self):
        messenger.send(EVENT_NAMES.GOTO_MAIN_MENU)

    def toggle_fullscreen(self, status):
        set_fullscreen_value(status == 1)

    def toggle_fps_counter(self, status):
        set_fullscreen_value(status == 1)

    def update_sfx_volume(self):
        value = self.sfx_volume_slider["value"]
        set_sfx_volume(value/100)

    def update_music_volume(self):
        value = self.music_volume_slider["value"]
        set_music_volume(value/100)

    def play_sample_sound(self):
        sample_sfx = base.loader.loadSfx(join("assets", "sfx", "sample.wav"))
        sample_sfx.play()

    def update_fps(self, status):
        set_fps_counter_enabled(status == 1)
