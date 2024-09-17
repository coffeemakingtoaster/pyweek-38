from os.path import join

from direct.particles.ParticleEffect import ParticleEffect

# load_model will assume that the model is under
# /assets/models/<name>/<name>.obj
def load_model(name):
    model = loader.loadModel(join("assets","models",name, name+".bam"))
    
    #texture = loader.loadTexture("assets/models/"+name+"/"+name+".jpeg")
    #model.setTexture(texture)
    return model
def load_mapObj(name):
    model = loader.loadModel(join("assets","models/MapObjects",name,name+".bam"))
    return model

def load_particles(name):
   p = ParticleEffect()
   p.loadConfig(join("assets","particles",name, "{}.ptf".format(name))) 
   return p

def load_font(name):
   if 'loader' in locals():
      return loader.loadFont(join("assets","fonts",f"{name}.ttf"))
