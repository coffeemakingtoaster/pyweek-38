from entities.item_base import ItemBase
from helpers.dish_helper import add_ingredient
from direct.particles.ParticleEffect import ParticleEffect


class Dish(ItemBase):
    def __init__(self, id, model):
        super().__init__(id, model)

        
        self.finished = False
        self.goodSalt = False
        self.badSalt = False
        self.spiced = False
        self.burned = False
        
        
            

    def add_ingredient(self, ingredient):
        return add_ingredient(self, ingredient)
    
    def apply_effects(self):
        if self.goodSalt:
            saltEffect = ParticleEffect()
            saltEffect.loadConfig("assets/particles/salt/salt.ptf")
            saltEffect.start(self.model,self.model)
        