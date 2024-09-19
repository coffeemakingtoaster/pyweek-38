from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math


from entities.entity_base import EntityBase



class Station(EntityBase):
    def __init__(self,name,actor):
        super().__init__()
        
        self.name = name
        self.model = actor
       
        
    
    
    def play_anim(self,anim):
        self.model.play(anim)

    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()

    
    def interact(self,item,player):
        print("Interact: "+ self.name)
    
    
    
    
    
    