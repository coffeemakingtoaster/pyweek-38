from os.path import join
import uuid
import random
from direct.task.TaskManagerGlobal import taskMgr

from entities.entity_base import EntityBase
from helpers.model_helpers import load_sounds

class Station(EntityBase):
    def __init__(self,name,actor):
        super().__init__()
        
        self.name = name
        self.model = actor
        self.task = None
        self.uuid = str(uuid.uuid4())
        self.sounds = []

        self.error_sounds = load_sounds("error")
    
    def play_anim(self,anim):
        self.model.play(anim)

    def play_sound(self, looping=False):
        if len(self.sounds) == 0:
            return
        sound = random.choice(self.sounds)
        if looping:
            sound.setLoop(True)
        sound.play()
    
    def play_error_sound(self):
        random.choice(self.error_sounds).play()

    def stop_sound(self):
        for sound in self.sounds:
             sound.stop()

    def destroy(self):
        self.ignoreAll()
        if self.model is not None:
            self.model.cleanup()
            self.model.removeNode()
        if self.task is not None:
            taskMgr.remove(self.task)
        for sound in self.sounds:
            sound.stop()
    
    def interact(self,item,player):
        pass

    def ai_interact(self,item,enemy):
        self.interact(item,enemy)
        
    def unset_interact(self,player):
        return

    def contains_uuid(self,uuid):
        return False
