from entities.item_base import ItemBase


class Ingredient(ItemBase):
    def __init__(self, id, model):
        super().__init__(id, model)

        self.finished = False
