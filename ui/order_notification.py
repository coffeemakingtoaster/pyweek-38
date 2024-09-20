from panda3d.core import TransparencyAttrib, TextNode
from direct.gui.DirectGui import DirectLabel, OnscreenImage

from os.path import join



class OrderNotifcation:
    def __init__(self, order) -> None:

        self.id = order.id
        self.font = loader.loadFont("assets/fonts/IndieFlower-Regular.ttf")

        self.image = OnscreenImage(
            scale=( 
                    0.2,
                    1,
                    0.2
                ),
                pos=(-2, 0, 0.95),
                image=join("assets", "images", "hud", f"order_notification_backplate.png")
            )
        self.image.setTransparency(TransparencyAttrib.MAlpha)

        self.review_label = DirectLabel(
                text=order.wanted_dish,
                scale=0.05,
                pos=(0,0,0),
                text_fg=(0,0,0,1),
                relief=None, 
                text_bg=(0,0,0,0),
                text_align=TextNode.ACenter,
                text_font=self.font
            )

        self.is_dead = False
  
    def destroy(self):
        self.image.remove_node()
        self.review_label.remove_node()
        self.is_dead = True

    def set_pos(self, pos):
        self.image.setPos(
            pos
        )

        self.review_label.setPos(
            self.image.getPos()[0] - self.image.getScale()[0] + 0.18,
            self.image.getPos()[1],
            self.image.getPos()[2]
        )

    def get_side_offset(self):
        return (self.image.getScale()[0])
