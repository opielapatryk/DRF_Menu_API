from domain.entities.dish import Dish
from application.serializer import DishSerializer

def test_serializer_domain_dish():
    dish = Dish(1,'pizza','italian dish',2.99)

    expected_data = {
        "id": 1,
        "name": "pizza",
        "description": "italian dish",
        "price": 2.99
        }
    
    serializer = DishSerializer(dish)

    assert serializer.data == expected_data
    