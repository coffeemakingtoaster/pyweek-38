from typing import List
from panda3d.core import TextNode, TransparencyAttrib

from direct.gui.DirectGui import DirectLabel, OnscreenImage

from direct.showbase.ShowBase import messenger
from constants.events import EVENT_NAMES
from entities.dish import Dish
from helpers.model_helpers import load_font
from ui.order_notification import OrderNotifcation
from ui.review_backplate import ReviewDisplay
from ui.ui_base import ui_base

from helpers.review_generator import TEAM, Review

import random
from os.path import join

class hud(ui_base):
    def __init__(self):
        super().__init__()

        self.font = load_font('Rubik-Light')

        self.reviews: List[ReviewDisplay] = []
        self.orders: List[OrderNotifcation] = []

        self.accept(EVENT_NAMES.DISPLAY_REVIEW, self.__display_review)
        self.accept(EVENT_NAMES.SHOW_PLAYER_ORDER, self.__display_order)
        self.accept(EVENT_NAMES.HIDE_PLAYER_ORDER, self.__hide_order)
        self.accept(EVENT_NAMES.ADD_SCORE, self.__add_score)
        self.accept("5", self.__send_win)
        self.accept("6", self.__send_lose)

        self.player_score = 0
        self.enemy_score = 0

        enemy_score_image = OnscreenImage(
            scale=( 
                    0.17,
                    1,
                    0.04
                ),
                pos=(1.35, 0, -0.9),
                image=join("assets", "images", "hud", f"enemy_score_display.png")
        )
        enemy_score_image.setTransparency(TransparencyAttrib.MAlpha)

        self.ui_elements.append(enemy_score_image)

        self.enemy_score_display = DirectLabel(
                text=f"{self.enemy_score}",
                scale=0.05,
                pos=(1.35,0,-0.91),
                text_fg=(0,0,0,1),
                relief=None, 
                text_bg=(0,0,0,0),
                text_align=TextNode.ACenter,
                text_font=self.font
            )
        self.ui_elements.append(self.enemy_score_display)

        player_score_image = OnscreenImage(
            scale=( 
                    0.17,
                    1,
                    0.04
                ),
                pos=(-1.35, 0, -0.9),
                image=join("assets", "images", "hud", f"player_score_display.png")
        )

        player_score_image.setTransparency(TransparencyAttrib.MAlpha)

        self.ui_elements.append(player_score_image)

        self.player_score_display = DirectLabel(
                text=f"{self.player_score}",
                scale=0.05,
                pos=(-1.35,0,-0.91),
                text_fg=(0,0,0,1),
                relief=None, 
                text_bg=(0,0,0,0),
                text_align=TextNode.ACenter,
                text_font=self.font
            )
        self.ui_elements.append(self.player_score_display)

    def destroy(self):
        super().destroy()
        for rev in self.reviews:
            rev.destroy()
        self.reviews = []
        for order in self.orders:
            order.destroy()
        self.orders = []

    def __debug_player(self):
        messenger.send(
            EVENT_NAMES.FINISH_ORDER,[
            Dish.init_from_scratch(
                "Pizza",
                None,
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
            ),
            True 
        ])

    def __debug_enemy(self):
        messenger.send(EVENT_NAMES.ADD_ORDER,["Pizza"])

        messenger.send(EVENT_NAMES.FINISH_ORDER,[
            Dish.init_from_scratch(
                "Pizza",
                None,
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
            ),
            False 
        ])

    def __display_review(self, review: Review):
        if len(self.reviews) == 3:
            self.reviews.pop().gracefully_destroy_review(True)

        new_review = ReviewDisplay(review)
        self.reviews.insert(0,new_review)
        
        offset = 0
        for i in range(len(self.reviews)):
            if self.reviews[i].is_dead:
                continue
            self.reviews[i].set_pos((
                1.2,
                0,
                0.8 - offset - self.reviews[i].get_bottom_offset()
            ))
            offset += (self.reviews[i].get_bottom_offset() * 2) + 0.05
        self.__add_score(review.star_count, review.team,review.shittiness_score)

    def __display_order(self, order):
        if len(self.orders) == 2:
            self.orders.pop().destroy()

        new_order = OrderNotifcation(order)
        self.orders.insert(0,new_order)

        self.__render_orders()

    def __render_orders(self):
        offset = 0
        for i in range(len(self.orders)):
            if self.orders[i].is_dead:
                continue
            self.orders[i].set_pos((
                - 1.8  + offset + self.orders[i].get_side_offset(),
                0,
                0.8
            ))
            offset += (self.orders[i].get_side_offset() * 2) + 0.05

    def __hide_order(self, id):
        for i in range(len(self.orders)):
            if self.orders[i].id == id:
                o = self.orders.pop(i)
                o.destroy()
                break
        self.__render_orders()

    def __send_win(self):
        messenger.send(EVENT_NAMES.GAME_VICTORY, [self.player_score, self.enemy_score])

    def __send_lose(self):
        messenger.send(EVENT_NAMES.GAME_OVER, [True])

    def __add_score(self, score, team,shitty):
        if team == TEAM.ENEMY:
            self.enemy_score += (score * 10) -shitty
        else:
            self.player_score += (score * 10) -shitty
        # there seems to be a weird bug within panda3d that sometimes causes this to fail
        # Worst case: we update it again sometime else
        if self.player_score >= 250:
            self.__send_win()
            return
        if self.enemy_score >= 250:
            self.__send_lose()
            return
        try:
            self.player_score_display["text"] = f"{int(self.player_score)}"
            self.enemy_score_display["text"] = f"{int(self.enemy_score)}"
        except:
            pass
