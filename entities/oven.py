from direct.actor.Actor import Actor
from panda3d.core import Vec3

import math
from entities.station import Station

class Oven(Station):
    def __init__(self,actor):
        self.id = "Oven"
        self.duration = 10
        
        
        
        super().__init__(id,actor)
    
    def interact(self,item):
        
        if item.id == "raw_pizza":
            print("Yay Pizza")
            self.inventory.append(item)
            self.play_anim("Open")
            self.play_anim("Closed")
            #domethodlater(duration,finishcooking)
        else:
            #Error Sound
            print("I only eat pizza :()")
            
            

