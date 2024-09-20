from direct.showbase.ShowBase import messenger
from constants.events import EVENT_NAMES
from constants.map import PATHFINDING_MAP
from helpers.pathfinding_helper import grid_pos_to_global, pos_to_string

class Field:
    cords = None
    status = None
    owner = None
    corresponding_station_uuid = None
    
    def __init__(self, cords, status=False, owner=None, corresponding_station_uuid=None) -> None:
        self.cords = cords
        self.status = status
        self.owner = owner
        self.corresponding_station_uuid = corresponding_station_uuid

    def _determine_uuid(self, station_handler):
        print("trying to autodetect closest item uuid. Result: ",end="")
        station = station_handler.get_closest_station_by_type(
            grid_pos_to_global(self.cords),
            PATHFINDING_MAP[self.cords[0]][self.cords[1]]
        )
        if station is None:
            return
        self.corresponding_station_uuid = station.uuid

    def update(self, status, owner, corresponding_station_uuid=None) -> None:
        self.status = status
        self.owner = owner
        if corresponding_station_uuid is not None:
            print(f"Set uuid for {self.cords}")
            self.corresponding_station_uuid = corresponding_station_uuid

class UsageHandler:
    def __init__(self) -> None:
        self.state = {} 
        self.station_handler = None

    def set_station_handler(self, station_handler):
        self.station_handler = station_handler

    def get_cord_status(self, cords, uuid=None):
        cord_formatted = pos_to_string(cords)
        if cord_formatted not in self.state:
            self.state[cord_formatted] = Field(cords)
            if self.station_handler is not None:
                self.state[cord_formatted]._determine_uuid(self.station_handler)
        return self.state[cord_formatted]

    def set_status_by_uuid(self, uuid, status, owner_id=None, cords=None):
        if cords is not None:
            res = self.get_cord_status(cords)
            if res is not None:
                print("merged notes")
                res.update(status, owner_id, uuid)
                return
        for key in self.state.keys():
            element = self.state[key]
            if element.corresponding_station_uuid == uuid:
                element.update(status, owner_id)
                # Notify npcs
                self.__notify_of_takeover(element.cords)
                return True
        print("Could not find station by uuid")
        return False
    
    def __notify_of_takeover(self, cords):
        messenger.send(EVENT_NAMES.RECALCULATE_WAYPOINTS, [cords])

    def set_cord_status(self, cords, status, owner_id, corresponding_station_uuid=None):
        cord_formatted = pos_to_string(cords)
        if cord_formatted not in self.state:
            if corresponding_station_uuid is not None:
                if self.set_status_by_uuid(corresponding_station_uuid, status, owner_id, cords):
                    return
            self.state[cord_formatted] = Field(cords, status, owner_id, corresponding_station_uuid)
            # if not provided: try to autodectect uuid
            if self.station_handler is not None and corresponding_station_uuid is None:
                self.state[cord_formatted]._determine_uuid(self.station_handler)
        else:
            self.state[cord_formatted].update(status, owner_id,corresponding_station_uuid)
            if corresponding_station_uuid is not None:
                self.set_status_by_uuid(corresponding_station_uuid, status, owner_id)
