from typing import List
from constants.map import TARGETS
from entities.station import Station
from panda3d.core import Vec3, Point3
from heapq import heappop, heappush

class StationHandler:
    def __init__(self, stations: List[Station]) -> None:
        self.stations: List[Station] = stations

    def get_closest_station_by_type(self, position: Point3, target: TARGETS) -> Station | None:
        viable_choices = [] 
        for station in self.stations:
            if station.name != target:
                continue
            heappush(
                viable_choices, 
                (Vec3(position.x - station.model.getPos().x,position.y - station.model.getPos().y,0).length(), station)
            )
        if len(viable_choices) == 0:
            return None
        return heappop(viable_choices)[1]

    def get_closest_station(self, position: Point3) -> Station | None:
        viable_choices = [] 
        for station in self.stations:
            heappush(
                viable_choices, 
                (Vec3(position.x - station.model.getPos().x, position.y - station.model.getPos().y, 0).length(), station)
            )
        if len(viable_choices) == 0:
            return None
        return heappop(viable_choices)[1]

    def get_station_by_uuid(self, uuid: str) -> Station | None:
        for station in self.stations:
            if station.uuid == uuid:
                return station
        return None
