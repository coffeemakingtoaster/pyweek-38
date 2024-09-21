from panda3d.core import *
from helpers.model_helpers import load_model

class ProgressBar():
    def __init__(self, model, duration,evil,player):
        self.model = model
        self.duration = duration
        self.evil = evil
        self.player = player
        if evil == 1:
            player.is_evil = True
        
        #self.progress_bar_background = load_model("timer_bg")
        #self.progress_bar_background.reparentTo(self.model)
        #self.progress_bar_background.setHpr(Vec3(0,0,0)-self.model.getHpr())
        #self.progress_bar_background.setPos(0, 0, 0.3)  

        
        self.progress_bar_foreground = load_model("timer_fg")
        self.progress_bar_foreground.reparentTo(self.model)
        self.progress_bar_foreground.setHpr(Vec3(0,0,0)-self.model.getHpr())
        self.progress_bar_foreground.setPos(0, 0, 1.5-self.model.getZ()+(evil*0.3))
        self.progress_bar_foreground.setLightOff(1)
        self.progress_bar_foreground.setColor(0+evil,0.5-evil,0,1)  

        # Start task to update the progress bar over time
        self.update_task = taskMgr.add(self.update, "updateProgressBar")
        
    def update(self, task):
        
        time_elapsed = task.time
        progress = time_elapsed / self.duration

        
        progress = max(0.1, min(progress, 1))

        
        if not self.progress_bar_foreground.isEmpty():
            self.progress_bar_foreground.setScale(progress, 1, 1)

        
        if time_elapsed >= self.duration:
            return task.done
        return task.cont

    def destroy(self):
        
        if self.evil:
            self.player.is_evil = False
        
        #if self.progress_bar_background:
        #    self.progress_bar_background.removeNode()
        #    self.progress_bar_background = None

        if self.progress_bar_foreground:
            self.progress_bar_foreground.removeNode()
            self.progress_bar_foreground = None

        
        if hasattr(self, 'update_task'):
            taskMgr.remove(self.update_task)