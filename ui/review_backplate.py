from panda3d.core import TransparencyAttrib, TextNode
from direct.gui.DirectGui import DirectFrame, DirectLabel, OnscreenImage
from direct.showbase.ShowBase import taskMgr
from direct.task import Task
from helpers.model_helpers import load_font
from helpers.review_generator import Review

from os.path import join

TEXT_WRAP = 17

__base = 0.07
HEIGHT_MAP = {
    's':__base,
    'm':1.605042017 * __base,
    'l':2.319327731 * __base
} 

OFFSET_MAP = {
    's': 0.024,
    'm': 0.019,
    'l': - 0.05 
}

font = load_font('Rubik-Light')

# This would have been better when just wrapping all of it in a frame...but anyways who cares
class ReviewDisplay:
    def __init__(self, review: Review) -> None: 

        print(f"review for {review.team}")

        self.font = loader.loadFont("assets/fonts/Rubik-Light.ttf")

        review_text=f"{review.review_text}"

        user_name=f"{review.user_name}"

        if len(review_text) > 150:
            review_text = f"{review_text[:145]}..."

        if len(user_name) > 10:
            user_name = f"{user_name[:7]}..."

        self.image = OnscreenImage(
            scale=( 
                    0.5,
                    1,
                    HEIGHT_MAP[self.__get_size(review_text)]
                ),
                pos=(-1.35, 0, 0.95),
                image=join("assets", "images", "hud", f"review_backplate_{self.__get_size(review_text)}_{review.team}.png")
            )

        self.review_label = DirectLabel(
                text=review_text,
                scale=0.05,
                pos=(0,0,0),
                text_fg=(0,0,0,1),
                relief=None, 
                text_bg=(0,0,0,0),
                text_wordwrap=TEXT_WRAP,
                text_align=TextNode.ALeft,
                text_font=self.font
            )

        self.username_label = DirectLabel(
                text=user_name,
                scale=0.05,
                pos=(-1,0,-1),
                text_fg=(0,0,0,1),
                relief=None, 
                text_bg=(0,0,0,0),
                text_wordwrap=TEXT_WRAP,
                text_align=TextNode.ACenter,
                text_font=self.font
            )

        self.image.setTransparency(TransparencyAttrib.MAlpha)

        self.review = review

        self.rating_frame = self.__build_rating_frame()

        self.task = taskMgr.doMethodLater(15, self.gracefully_destroy_review, "destroy")
        self.is_dead = False

    def __build_rating_frame(self):
        frame = DirectFrame(pos=(0,0,0),frameColor=(0,0,0,1),frameSize=())

        # Keep a reference to save them from the garbage collector
        self.star_images = []
        
        i = 0
        while i < self.review.star_count:
            self.star_images.append(
                OnscreenImage(
                    scale=( 
                        0.03,
                        0.03,
                        0.03
                    ),
                    pos=((0.06 * i), 0, 0),
                    image=join("assets", "images", "hud", f"star.png")
                )
            )
            i+=1
        
        if self.review.star_count%1 != 0:
            self.star_images.append(
                OnscreenImage(
                    scale=( 
                        0.03/2,
                        0.03,
                        0.03
                    ),
                    pos=((0.06 * (i - 1))+0.04, 0, 0),
                    image=join("assets", "images", "hud", f"half_star.png")
                )
            )

        for img in self.star_images:
            img.setTransparency(TransparencyAttrib.MAlpha)
            img.reparentTo(frame)

        return frame

    def __get_size(self,text: str):
        if len(text) < TEXT_WRAP * 2:
            return 's'
        if len(text) < TEXT_WRAP * 4.5:
            return 'm'
        return 'l'
    
    def gracefully_destroy_review(self, prematurely=False):
        if prematurely:
            taskMgr.remove(self.task)
        self.image.remove_node()
        self.review_label.remove_node()
        self.username_label.remove_node()
        self.rating_frame.remove_node()
        for img in self.star_images:
            img.remove_node()
        self.is_dead = True
        return Task.done

    def destroy(self):
        taskMgr.remove(self.task)
        self.image.remove_node()
        self.review_label.remove_node()
        self.username_label.remove_node()
        self.rating_frame.remove_node()
        for img in self.star_images:
            img.remove_node()
        self.is_dead = True

    def set_pos(self, pos):
        
        self.image.setPos(
            pos
        )

        self.review_label.setPos(
            self.image.getPos()[0] - self.image.getScale()[0] + 0.05,
            self.image.getPos()[1],
            self.image.getPos()[2] - OFFSET_MAP[self.__get_size(self.review_label['text'])]
        )

        self.username_label.setPos(
            self.image.getPos()[0] - 0.3,
            self.image.getPos()[1],
            self.image.getPos()[2] + self.image.getScale()[2] - 0.04
        )

        self.rating_frame.setPos(
            self.image.getPos()[0] + 0.2,
            self.image.getPos()[1],
            self.image.getPos()[2] + self.image.getScale()[2] - 0.03
        )

    def get_bottom_offset(self):
        return (self.image.getScale()[2])
    
    def print(self):
        self.review.print()
