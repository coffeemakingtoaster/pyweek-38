from direct.showbase import DirectObject

from panda3d.core import TextFont 

from direct.gui.DirectGui import OnscreenImage

from os.path import join

class ui_base(DirectObject.DirectObject):
    def __init__(self):
        
        super().__init__()
        
        self.ui_elements = []
        
    def destroy(self):
        for ui_element in self.ui_elements:
            #print("destroying ui element")
            ui_element.destroy()
            ui_element.removeNode()

    def hide(self):
        for ui_element in self.ui_elements:
            #print("hiding ui element")
            if ui_element is not None:
                ui_element.hide()
        self.ui_elements = []
        
    def load_background_image(self):
        background = OnscreenImage(join("assets", "images","main_menu_background.png"), pos=(-0.1,0,0), scale=(1521 * 0.0012,1,859 * 0.0012)) 
        self.ui_elements.append(background)
