from panda3d.core import TransparencyAttrib, TextNode
from direct.gui.DirectGui import DirectLabel, OnscreenImage
from direct.showbase.ShowBase import taskMgr
from direct.task import Task
from helpers.model_helpers import load_font
from helpers.review_generator import Review

from os.path import join

TEXT_WRAP = 17

HEIGHT_MAP = {
    's':0.05,
    'm':0.1,
    'l':0.2
} 

font = load_font('Rubik-Light')

class ReviewDisplay:
    def __init__(self, review: Review) -> None:
        review_text=f"{review.review_text}"

        self.font = load_font('Rubik-Light')

        user_name=f"{review.user_name}"

        if len(review_text) > 150:
            review_text = f"{review_text[:145]}..."

        if len(user_name) > 10:
            user_name = f"{user_name[:7]}..."

        self.review_label = DirectLabel(
                text=review_text,
                scale=0.05,
                pos=(0,0,0),
                text_fg=(255,0,0,1),
                relief=None, 
                text_bg=(0,0,0,0),
                text_wordwrap=TEXT_WRAP,
                text_align=TextNode.ACenter,
                text_font=self.font
            )

        self.image = OnscreenImage(
            scale=( 
                    0.5,
                    1,
                    HEIGHT_MAP[self.__get_size(review_text)]
                ),
                pos=(-1.35, 0, 0.95),
                image=join("assets", "images", "hud", f"review_backplate_{self.__get_size(review_text)}.png")
            )

        self.username_label = DirectLabel(
                text=user_name,
                scale=0.05,
                pos=(-1,0,-1),
                text_fg=(255,0,0,1),
                relief=None, 
                text_bg=(0,0,0,0),
                text_wordwrap=TEXT_WRAP,
                text_align=TextNode.ACenter,
                text_font=self.font
            )

        self.image.setTransparency(TransparencyAttrib.MAlpha)

        self.task = taskMgr.doMethodLater(5, self.gracefully_destroy_review, "destroy")
        self.is_dead = False
        self.review = review
    
    def __get_size(self,text: str):
        if len(text) < TEXT_WRAP * 2:
            return 's'
        if len(text) < TEXT_WRAP * 4:
            return 'm'
        return 'l'
    
    def gracefully_destroy_review(self, prematurely=False):
        if prematurely:
            taskMgr.remove(self.task)
        self.image.destroy()
        self.review_label.destroy()
        self.username_label.destroy()
        self.is_dead = True
        return Task.done

    def destroy(self):
        taskMgr.remove(self.task)
        self.image.remove()
        self.review_label.remove()
        self.username_label.remove()
        self.is_dead = True

    def set_pos(self, pos):
        
        self.image.setPos(
            pos
        )

        self.review_label.setPos(
            self.image.getPos()[0],
            self.image.getPos()[1],
            self.image.getPos()[2] + max(self.image.getScale()[2] / 4, 0.01)
        )

        self.username_label.setPos(
            self.image.getPos()[0] - 0.2,
            self.image.getPos()[1],
            self.image.getPos()[2] + max(self.image.getScale()[2]/ 2.5 , 0.01)
        )

    def get_bottom_offset(self):
        return (self.image.getScale()[2])
    
    def print(self):
        self.review.print()
