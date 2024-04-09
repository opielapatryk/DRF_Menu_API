import pytest
from domain.entities.dish import Dish
from domain.use_cases.dish_post_use_case import dish_post_use_case
from unittest import mock

@pytest.fixture
def domain_dishes():
    dish_1 = Dish(
        id=1,
        name='pizza',
        description='italiano sepcailze',
        price=9.99
    )
    dish_2 = Dish(
        id=2,
        name='spagetti',
        description='italiano pasta',
        price=14.99
    )
    dish_3 = Dish(
        id=3,
        name='nalesniki',
        description='Something sweet',
        price=7.99,
    )
    dish_4 = Dish(
        id=4,
        name='chips',
        description='fried potatooo',
        price=3.29
    )

    return [dish_1, dish_2, dish_3, dish_4]



def test_post_dish(domain_dishes):
    dish = Dish(id=5,name='chips',description='fried potatooo',price=33.29)
    repo = mock.Mock()
    repo.post.return_value = domain_dishes + [dish]

    
    result = dish_post_use_case(repo, dish)

    repo.post.assert_called_with(dish)
    assert result == domain_dishes + [dish]