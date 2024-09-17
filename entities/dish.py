from entities.item_base import ItemBase
from helpers.dish_helper import add_ingredient


class Dish(ItemBase):
    def __init__(self, id, model):
        super().__init__(id, model)

        self.finished = False
        self.salted = 0.0
        self.spiced = 0.0
        self.bad_dish = False

    def add_ingredient(self, ingredient):
        add_ingredient(self, ingredient)
