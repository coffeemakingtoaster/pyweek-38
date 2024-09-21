import uuid
from direct.showbase.ShowBase import taskMgr
from direct.task.Task import Task

from direct.showbase.DirectObject import DirectObject, messenger

from constants.events import EVENT_NAMES
from entities.dish import Dish
from helpers.dish_helper import VIABLE_FINISHED_ORDER_DISHES
from helpers.review_generator import Review

from time import time

import random

class Order:
    order_time = time() 
    wanted_dish = None
    allowed_time = 100_000
    id=None

    def __init__(self, wanted_dish, allowed_time=100_000) -> None:
        self.wanted_dish = wanted_dish
        self.order_time = time()
        self.allowed_time = allowed_time
        self.id = str(uuid.uuid4())

    def is_too_late(self):
        return int(time() - self.order_time) > self.allowed_time

class OrderHandler(DirectObject):
    def __init__(self) -> None:
        super().__init__()
        self.enemy_orders = []
        self.player_orders = []

        self.enemy_orders = [
            Order("Pizza"), Order("Pizza"),
            Order("Pizza"),
        ]

        self.accept(EVENT_NAMES.FINISH_ORDER, self.__finish_order)
        self.accept(EVENT_NAMES.ADD_ORDER, self.__add_order)

        self.__generate_player_order()
        
        # This should fill the order queue in the beginning. Afterwards it should not do anything
        self.bg_task = taskMgr.doMethodLater(50, self.__generate_player_order, "scheduled_player_order_generator")

    def destroy(self):
        self.player_orders = []
        self.enemy_orders = []
        taskMgr.remove(self.bg_task)
        self.ignoreAll()

    def __generate_player_order(self, _=None):
        if len(self.player_orders) > 1:
            return Task.again

        order =Order(
                getattr(
                    VIABLE_FINISHED_ORDER_DISHES,
                    random.choice(
                        [a for a in dir(VIABLE_FINISHED_ORDER_DISHES) if not a.startswith('__') and not callable(getattr(VIABLE_FINISHED_ORDER_DISHES, a))]
                    )
                )
            )
        self.player_orders.append(order)
        messenger.send(EVENT_NAMES.SHOW_PLAYER_ORDER, [order])
        return Task.again

    # This is used for the enemies to be able to report that they started a dish
    def __add_order(self, dishId: str):
        self.enemy_orders.append(
            Order(
                dishId
            )
        )
        print(f"Added a {dishId} order for enemies")

    def __get_order(self, dish, is_from_player):
        print(f"{is_from_player} player??")
        if is_from_player:
            for i in range(len(self.player_orders)):
                print(f"{dish.id} {self.player_orders[i].wanted_dish}")
                if self.player_orders[i].wanted_dish == dish.id:
                    return self.player_orders.pop(i)
        else:
            for i in range(len(self.enemy_orders)):
                if self.enemy_orders[i].wanted_dish == dish.id:
                    return self.enemy_orders.pop(i)
        return None

    def __finish_order(self, dish: Dish, is_from_player):
        if (order := self.__get_order(dish, is_from_player)) is not None:
            dish.is_late = order.is_too_late()
            review = Review.fromDish(dish, is_from_player)
            messenger.send(EVENT_NAMES.DISPLAY_REVIEW, [review])
            if is_from_player:
                messenger.send(EVENT_NAMES.HIDE_PLAYER_ORDER, [order.id])
                self.__generate_player_order()
        else:
            print("Finished order did not match known order")
