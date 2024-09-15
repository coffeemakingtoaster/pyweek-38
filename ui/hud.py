
from direct.showbase.ShowBase import messenger
from constants.events import EVENT_NAMES
from ui.ui_base import ui_base

from helpers.review_generator import Review


class hud(ui_base):
    def __init__(self):
        super().__init__()

        # TODO: setup hud

        self.reviews = []

        messenger.accept(EVENT_NAMES.DISPLAY_POSITIVE_REVIEW, self.__add_positive_review)
        messenger.accept(EVENT_NAMES.DISPLAY_NEGATIVE_REVIEW, self.__add_negative_review)

        messenger.accept("5", self.__debug_pos)
        messenger.accept("6", self.__debug_neg)

    def __debug_neg(self):
        messenger.send(EVENT_NAMES.DISPLAY_NEGATIVE_REVIEW)

    def __debug_pos(self):
        messenger.send(EVENT_NAMES.DISPLAY_POSITIVE_REVIEW)

    def __add_positive_review(self):
        print("positive")

    def __add_negative_review(self):
        print("positive")

    def __display_review(self, review: Review):
        print(review)
        if len(self.reviews) == 3:
            oldest = self.reviews.pop()
            oldest.destroy()
        self.reviews.insert(0, review)
