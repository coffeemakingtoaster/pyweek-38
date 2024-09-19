from direct.actor.Actor import Actor
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec3

import math


from entities.entity_base import EntityBase



class Station(EntityBase):
    def __init__(self,name,actor):
        super().__init__()
        
        self.name = name
        self.model = actor
        self.task = None
    
    def play_anim(self,anim):
        self.model.play(anim)

    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()
        if self.task is not None:
            taskMgr.remove(self.task)

    
    def interact(self,item,player):
        print("Interact: "+ self.name)
    
    
    
    
    
    
