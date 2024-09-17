
import json
from helpers.model_helpers import load_model, load_mapObj
from panda3d.core import *
from entities.station import Station
from entities.oven import Oven
from direct.actor.Actor import Actor

def load_map(json_data):
    
    objects = json_data["Objects"]
    models = []
    lights = []
    stations = []
    

    for obj in objects:
        name = obj["name"]
        position = obj["position"]
        rotation = obj["rotation"]
        
        if name == "Dot":
            slight = Spotlight('slight')
            slight.setColor((2.5, 2.5, 1.5, 0))
            lens = PerspectiveLens()
            slight.setLens(lens)
            slnp = render.attachNewNode(slight)
            slnp.setPos(position["x"], position["y"], 10)
            slnp.setHpr(0,-90,0)
            render.setLight(slnp)
            lights.append(slnp)
        elif name == "Oven":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Open": "assets/models/MapObjects/"+name+"/"+name+"-Open.bam","Close":"assets/models/MapObjects/"+name+"/"+name+"-Close.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.reparentTo(render)
            stations.append(Oven(actor))
        
        else:
        # Create a model instance for each object and add it to the list
            model = load_mapObj(name)
            model.setPos(position["x"],position["y"],position["z"])
            model.setH(rotation)
            model.reparentTo(render)
            models.append(model)
        

    return models , lights, stations