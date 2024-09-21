import uuid
from direct.task.TaskManagerGlobal import taskMgr

from entities.entity_base import EntityBase

class Station(EntityBase):
    def __init__(self,name,actor):
        super().__init__()
        
        self.name = name
        self.model = actor
        self.task = None
        self.uuid = str(uuid.uuid4())
    
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
        pass

    def ai_interact(self,item,enemy):
        self.interact(item,enemy)
        
    def unset_interact(self,player):
        return

    def contains_uuid(self,uuid):
        return False
