from panda3d.core import TransparencyAttrib, TextNode
from direct.gui.DirectGui import DirectLabel, OnscreenImage
from direct.showbase.ShowBase import taskMgr
from direct.task import Task

from os.path import join

class ReviewDisplay:
    def __init__(self, review) -> None:
        review_text=f"{review.user_name}: {review.review_text}"

        # cutoff
        if len(review_text) > 150:
            review_text = f"{review_text[:145]}..."

        self.label = DirectLabel(
                text=review_text,
                scale=0.05,
                pos=(0,0,0),
                text_fg=(255,0,0,1),
                relief=None, 
                text_bg=(0,0,0,0),
                text_wordwrap=17,
                text_align=TextNode.ACenter
            )

        self.image = OnscreenImage(
            scale= ( 
                0.5,
                1,
                max(min(0.2 * (len(review_text)/150), 0.2), 0.05)
                ),
                pos=(-1.35, 0, 0.95),
                image=join("assets", "images", "hud", "review_backplate.png")
            )

        self.image.setTransparency(TransparencyAttrib.MAlpha)

        self.task = taskMgr.doMethodLater(5, self.gracefully_destroy_review, "destroy")
        self.is_dead = False
        self.review = review

    def gracefully_destroy_review(self, prematurely=False):
        if prematurely:
            taskMgr.remove(self.task)
        self.image.destroy()
        self.label.destroy()
        self.is_dead = True
        return Task.done

    def destroy(self):
        taskMgr.remove(self.task)
        self.image.remove()
        self.label.remove()
        self.is_dead = True

    def set_pos(self, pos):
        
        self.image.setPos(
            pos
        )

        self.label.setPos(
            self.image.getPos()[0],
            self.image.getPos()[1],
            self.image.getPos()[2] + max(self.image.getScale()[2] / 4, 0.01)
        )

    def get_bottom_offset(self):
        return (self.image.getScale()[2])
    
    def print(self):
        self.review.print()
