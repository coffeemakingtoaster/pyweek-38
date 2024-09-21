from helpers.model_helpers import load_model

class VIABLE_FINISHED_ORDER_DISHES:
    SALAD = "finished_salad"
    STEAK = "finished_steak"
    SOUP = "plated_soup"
    PIZZA = "plated_pizza"
    ICE_CREAM = "plated_ice_cream"

# Used as a lookup map for what name should be displayed to the user
DISHES_PRETTY_NAMES_UWU = {
    VIABLE_FINISHED_ORDER_DISHES.SALAD: "salad",
    VIABLE_FINISHED_ORDER_DISHES.STEAK: "steak",
    VIABLE_FINISHED_ORDER_DISHES.SOUP: "soup",
    VIABLE_FINISHED_ORDER_DISHES.PIZZA: "pizza",
    VIABLE_FINISHED_ORDER_DISHES.ICE_CREAM: "ice cream"
}

def add_ingredient(dish, ingredient):
    match dish.id:
        case "empty_plate":
            match ingredient:
                case "fries":
                    transform("plated_fries", dish,False)
                    return True
                case "steak":
                    transform("plated_steak", dish,False)
                    return True
                case "chopped_tomato":
                    transform("plated_chopped_tomato", dish,False)
                    return True
                case "chopped_salad":
                    transform("plated_chopped_salad", dish,False)
                    return True
                case "pizza_dough":
                    transform("plated_pizza_dough", dish,False)
                    return True
                case "unplated_ice_cream":
                    transform("plated_ice_cream", dish,True)
                    return True
                case "unplated_soup":
                    transform("plated_soup", dish,True)
                    return True

        # Steak dish
        case "plated_fries":
            match ingredient:
                case "steak":
                    transform("finished_steak", dish,True)
                    return True
        case "plated_steak":
            match ingredient:
                case "fries":
                    transform("finished_steak", dish,True)
                    return True

        # Salad dish
        case "plated_chopped_tomato":
            match ingredient:
                case "chopped_salad":
                    transform("finished_salad", dish,True)
                    return True
        case "plated_chopped_salad":
            match ingredient:
                case "chopped_tomato":
                    transform("finished_salad", dish,True)
                    return True

        # pizza dish
        case "plated_pizza_dough":
            match ingredient:
                case "chopped_cheese":
                    transform("pizza_with_cheese", dish,False)
                    return True
                case "chopped_tomato":
                    transform("pizza_with_tomato", dish,False)
                    return True
        case "pizza_with_cheese":
            match ingredient:
                case "chopped_tomato":
                    transform("raw_pizza", dish,False)
                    return True
        case "pizza_with_tomato":
            match ingredient:
                case "chopped_cheese":
                    transform("raw_pizza", dish,False)
                    return True
        case "raw_pizza":
            match ingredient:
                case "unplated_pizza":
                    transform("plated_pizza", dish,True)
                    return True
    return False


def transform(dish_id, dish,finished):
    pos = dish.model.getPos()
    dish.model.removeNode()
    dish.model = load_model(dish_id)
    dish.finished = finished
    dish.model.setPos(pos)
    dish.model.reparentTo(render)
    dish.id = dish_id
    
