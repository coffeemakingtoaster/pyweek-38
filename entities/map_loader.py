
from constants.layers import MAP_COLLISION_BITMASK
from constants.map import MODEL_COLLISION_DIMENSION_LOOKUP, MODEL_COLLISION_OFFSET_LOOKUP 
from helpers.model_helpers import load_mapObj
from panda3d.core import *
from entities.oven import Oven
from entities.plate_station import Plate_Station
from direct.actor.Actor import Actor
from entities.Food_Station import Food_Station
from entities.Trash_Station import Trash_Station
from entities.CuttingBoard import CuttingBoard
from entities.ItemArea import ItemArea
from entities.freezer_door import FreezerDoor
from entities.Fry import Fry
from entities.pan import Pan
from entities.IceMaker import IceMaker
from entities.Pot import Pot

# dummy notifier. This is just needed as a param and doesnt actually do anythin :)
__notifier = CollisionHandlerEvent()

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
            __add_collision_box(element=actor, dimension=LVector3(0.45,0.38,2),offset=Point3(0.45,0.4,0.5))
            actor.reparentTo(render)
            stations.append(Oven(actor))
        elif name == "Washer":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Wash": "assets/models/MapObjects/"+name+"/"+name+"-Wash.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            __add_collision_box(element=actor, dimension=LVector3(0.61,0.5,1),offset=Point3(0.6,0.3,0))
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
            __add_collision_box(element=actor, dimension=LVector3(0.25,0.25,1),offset=Point3(0,0,0.5))
            actor.reparentTo(render)
            stations.append(Trash_Station(actor))
        elif name == "CuttingBoard":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Cut": "assets/models/MapObjects/"+name+"/"+name+"-Cut.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(CuttingBoard(actor))
        elif name == "ItemArea":
            actor = Actor("assets/models/empty_hands/empty_hands.bam")
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(ItemArea(actor))  
        elif name == "Fry":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam",{"Fry": "assets/models/MapObjects/"+name+"/"+name+"-Fry.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            __add_collision_box(element=actor, dimension=LVector3(0.25,0.4,2), offset=Point3(0.2,0.3,0))
            actor.reparentTo(render)
            stations.append(Fry(actor))
        elif name == "Pan":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam")
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(ItemArea(actor))  
        
        
        elif name == "Freezerdoor":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Open": "assets/models/MapObjects/"+name+"/"+name+"-Open.bam", "Close": "assets/models/MapObjects/"+name+"/"+name+"-Close.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(FreezerDoor(actor))
        elif name == "Storagedoor":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam", {"Open": "assets/models/MapObjects/"+name+"/"+name+"-Open.bam", "Close": "assets/models/MapObjects/"+name+"/"+name+"-Close.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(FreezerDoor(actor))
            stations.append(Pan(actor))
        elif name == "Pot":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam")
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(Pot(actor))
        elif name == "IceMaker":
            actor = Actor("assets/models/MapObjects/"+name+"/"+name+".bam",{"Close": "assets/models/MapObjects/"+name+"/"+name+"-Close.bam","Open": "assets/models/MapObjects/"+name+"/"+name+"-Open.bam"})
            actor.setPos(position["x"],position["y"],position["z"])
            actor.setH(rotation)
            actor.reparentTo(render)
            stations.append(IceMaker(actor))  
            
        else:
        # Create a model instance for each object and add it to the list
            model = load_mapObj(name)
            model.setPos(position["x"],position["y"],position["z"])
            model.setH(rotation)
            if name == "Floor":
                __add_wall_collision(model)
            elif name in MODEL_COLLISION_OFFSET_LOOKUP and name in MODEL_COLLISION_DIMENSION_LOOKUP:
                __add_collision_box(element=model, dimension=MODEL_COLLISION_DIMENSION_LOOKUP[name], offset=MODEL_COLLISION_OFFSET_LOOKUP[name])
            else:
                print(name)
            
            model.reparentTo(render)
            models.append(model)

    return models , lights, stations

def __add_wall_collision(element):
    # add walls inside the map
    __add_collision_box(element, LVector3(0.1,1.6,1), Point3(9.4,5.5,0))
    __add_collision_box(element, LVector3(0.1,0.5,1), Point3(9.4,2.5,0))
    __add_collision_box(element, LVector3(0.1,0.5,1), Point3(9.4,0.5,0))

    # add map borders
    __add_collision_plane(element, Point3(0,0,0),LVector3(1,0,0))
    __add_collision_plane(element, Point3(0,0,0),LVector3(0,1,0))
    __add_collision_plane(element, Point3(12,7.2,0),LVector3(-1,0,0))
    __add_collision_plane(element, Point3(12,7.2,0),LVector3(0,-1,0))


def __add_collision_plane(element, point: Point3, normal: LVector3, show=False):
    # setup hitboxes
    node = element.attachNewNode(CollisionNode(f"object_map_collision"))
    node.node().setCollideMask(MAP_COLLISION_BITMASK)
    node.setPos(0,0,0)
    if show:
        node.show()
    node.node().addSolid(CollisionPlane(LPlane(normal, point)))
    base.cTrav.addCollider(node, __notifier)

def __add_collision_box(element, dimension: LVector3, offset=Point3(0,0,0), show=False):
    # setup hitboxes
    node = element.attachNewNode(CollisionNode(f"object_map_collision"))
    node.node().setCollideMask(MAP_COLLISION_BITMASK)
    node.setPos(0,0,0)
    if show:
        node.show()
    node.node().addSolid(CollisionBox(offset,dimension.x, dimension.y, dimension.z))
    base.cTrav.addCollider(node, __notifier)
