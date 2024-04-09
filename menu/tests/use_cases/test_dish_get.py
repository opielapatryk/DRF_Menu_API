import pytest
from domain.entities.dish import Dish
from domain.use_cases.dish_get_use_case import dish_get_use_case
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



def test_get_dish(domain_dishes):
    repo = mock.Mock()
    repo.get.return_value = domain_dishes[0]

    result = dish_get_use_case(repo, 1)

    repo.get.assert_called_with(1)
    assert result == domain_dishes[0]