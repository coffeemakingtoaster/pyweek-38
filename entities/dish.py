from entities.item_base import ItemBase
from helpers.dish_helper import add_ingredient


class Dish(ItemBase):
    def __init__(self, id, model):
        super().__init__(id, model)

        self.finished = False
        self.goodSalt = False
        self.badSalt = False
        self.spiced = False
        self.burned = False

    def add_ingredient(self, ingredient):
        return add_ingredient(self, ingredient)
        