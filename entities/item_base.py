from abc import abstractmethod

from entities.entity_base import EntityBase


class ItemBase(EntityBase):

    def __init__(self, id, model):
        super().__init__()

        self.id = id
        self.model = model

    @abstractmethod
    def pick_up(self):
        pass

    @abstractmethod
    def put_down(self):
        pass