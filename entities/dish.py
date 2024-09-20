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
        self.saltEffect = None
        self.spiceEffect = None
        
        
            

    def add_ingredient(self, ingredient):
        return add_ingredient(self, ingredient)
    
    def apply_effects(self):
        print("Salt")
        if self.goodSalt:
           
            self.saltEffect = ParticleEffect()
            
            self.saltEffect.loadConfig("assets/particles/salt/salt.ptf")
            self.saltEffect.start(self.model, self.model)
            print("Hush")

        if self.badSalt:
            print("bad salt")
            
            self.saltEffect = ParticleEffect()
            self.saltEffect.loadConfig("assets/particles/salt/bad_salt.ptf")
            self.saltEffect.start(self.model, self.model)
        