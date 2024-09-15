from direct.showbase import DirectObject
from abc import abstractmethod


class EntityBase(DirectObject.DirectObject):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass
