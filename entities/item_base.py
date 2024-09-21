from abc import abstractmethod
import uuid

from entities.entity_base import EntityBase


class ItemBase(EntityBase):

    def __init__(self, id, model):
        super().__init__()

        self.id = id
        self.model = model
        self.uuid = str(uuid.uuid4())
        
    def apply_effects(self):
        return
