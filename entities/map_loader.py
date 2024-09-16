
import json
from helpers.model_helpers import load_model

def load_map(json_data):
    
    objects = json_data["Objects"]
    models = []
    

    for obj in objects:
        name = obj["name"]
        position = obj["position"]
        rotation = obj["rotation"]

        # Create a model instance for each object and add it to the list
        model = load_model(name)
        model.setPos(position["x"],position["y"],position["z"])
        model.setH(rotation)
        models.append(model)

    return models