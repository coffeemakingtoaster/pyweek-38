from helpers.model_helpers import load_model

did_it_add = False

def add_ingredient(dish, ingredient):
    match dish.id:
        case "empty_plate":
            match ingredient:
                case "fries":
                    transform("plated_fries", dish)
                case "steak":
                    transform("plated_steak", dish)
                case "chopped_tomato":
                    transform("plated_chopped_tomato", dish)
                case "chopped_salad":
                    transform("plated_chopped_salad", dish)
                case "pizza_dough":
                    transform("plated_pizza_dough", dish)
                case "unplated_ice_cream":
                    transform("plated_ice_cream", dish)
                case "unplated_soup":
                    transform("plated_soup", dish)
                case "unplated_pizza":
                    transform("plated_pizza", dish)
                


        # Steak dish
        case "plated_fries":
            match ingredient:
                case "steak":
                    transform("finished_steak", dish)
        case "plated_steak":
            match ingredient:
                case "fries":
                    transform("finished_steak", dish)

        # Salad dish
        case "plated_chopped_tomato":
            match ingredient:
                case "chopped_salad":
                    transform("finished_salad", dish)
        case "plated_chopped_salad":
            match ingredient:
                case "chopped_tomato":
                    transform("finished_salad", dish)

        # pizza dish
        case "plated_pizza_dough":
            match ingredient:
                case "chopped_cheese":
                    transform("pizza_with_cheese", dish)
                case "chopped_tomato":
                    transform("pizza_with_tomato", dish)
        case "pizza_with_cheese":
            match ingredient:
                case "chopped_tomato":
                    transform("raw_pizza", dish)
        case "pizza_with_tomato":
            match ingredient:
                case "chopped_cheese":
                    transform("raw_pizza", dish)

    return did_it_add


def transform(dish_id, dish):
    did_it_add = True
    pos = dish.model.getPos()
    dish.model.removeNode()
    dish.model = load_model(dish_id)
    dish.model.setPos(pos)
    dish.model.reparentTo(render)
    dish.id = dish_id
