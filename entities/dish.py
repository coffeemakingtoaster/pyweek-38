from entities.item_base import ItemBase
from helpers.dish_helper import add_ingredient
from direct.particles.ParticleEffect import ParticleEffect


class Dish(ItemBase):
    # This can be overwritten by the order handler
    is_late = False
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
        
    @staticmethod
    def init_from_scratch(id ,model, finished, badSalt, spiced, burned):
        dish = Dish(id, model)
        dish.finished = finished
        dish.badSalt = badSalt
        dish.spiced = spiced
        dish.burned = burned
        return dish
