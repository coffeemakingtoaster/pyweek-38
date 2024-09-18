
import json
from helpers.model_helpers import load_model, load_mapObj
from panda3d.core import *
from entities.station import Station
from entities.oven import Oven
from entities.plate_station import Plate_Station
from direct.actor.Actor import Actor
from entities.Food_Station import Food_Station
from entities.Trash_Station import Trash_Station
from entities.CuttingBoard import CuttingBoard
from entities.freezer_door import FreezerDoor

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
            slight.setColor((2, 2, 1, 0))
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
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Oven(actor))
        elif name == "Washer":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Plate_Station(actor))
        elif name == "Cheese_Station":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Food_Station(actor,"Cheese_Station","cheese"))
        elif name == "Chocolate_Station":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Food_Station(actor,"Chocolate_Station","chocolate"))
        elif name == "Dough_Station":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Food_Station(actor,"Dough_Station","pizza_dough"))
        elif name == "Ice_Station":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Food_Station(actor,"Ice_Station","ice_cubes"))
        elif name == "Onion_Station":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Food_Station(actor,"Onion_Station","onion"))
        elif name == "Potato_Station":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Food_Station(actor,"Potato_Station","potato"))
        elif name == "Salad_Station":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Food_Station(actor,"Salad_Station","salad"))
        elif name == "Steak_Station":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Food_Station(actor,"Steak_Station","raw_steak"))
        elif name == "Tomato_Station":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Food_Station(actor,"Tomato_Station","tomato"))
        elif name == "Trash":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Trash_Station(actor))
        elif name == "CuttingBoard":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Cut": "assets/models/MapObjects/"+name+"/"+name+"-Cut.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(CuttingBoard(actor))
        elif name == "Freezerdoor":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Open": "assets/models/MapObjects/"+name+"/"+name+"-Open.bam", "Close": "assets/models/MapObjects/"+name+"/"+name+"-Close.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(FreezerDoor(actor))
        else:
        # Create a model instance for each object and add it to the list
            model = load_mapObj(name)
            model.setPos(position["x"],position["y"],position["z"])
            model.setH(rotation)
            model.reparentTo(render)
            models.append(model)
        

    return models , lights, stations