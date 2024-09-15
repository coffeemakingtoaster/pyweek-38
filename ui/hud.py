from typing import List
from direct.showbase.ShowBase import messenger
from constants.events import EVENT_NAMES
from ui.review_backplate import ReviewDisplay
from ui.ui_base import ui_base

from helpers.review_generator import Review, get_review_for_food

import random

class hud(ui_base):
    def __init__(self):
        super().__init__()

        # TODO: setup hud
        self.reviews: List[ReviewDisplay] = []

        self.accept(EVENT_NAMES.DISPLAY_POSITIVE_REVIEW, self.__add_positive_review)
        self.accept(EVENT_NAMES.DISPLAY_NEGATIVE_REVIEW, self.__add_negative_review)

        self.accept("5", self.__debug_pos)
        self.accept("6", self.__debug_neg)

    def destroy(self):
        super().destroy()
        for rev in self.reviews:
            rev.destroy()

    def __debug_neg(self):
        messenger.send(EVENT_NAMES.DISPLAY_NEGATIVE_REVIEW)

    def __debug_pos(self):
        messenger.send(EVENT_NAMES.DISPLAY_POSITIVE_REVIEW)

    def __add_positive_review(self):
        self.__display_review(get_review_for_food(
           "Pizza",
            is_player_food=True
        ))

    def __add_negative_review(self):
        self.__display_review(
            get_review_for_food("Soup",
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False]),
                False
            )
        )

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
            offset += (self.reviews[i].get_bottom_offset() * 2) + 0.02

