from menu.domain.entities.dish import Dish

def test_dish():
    dish = Dish(1, "pizza", "pepperoni", 12.99)
    assert dish.id == 1
    assert dish.name == 'pizza'
    assert dish.description == 'pepperoni'
    assert dish.price == 12.99
    