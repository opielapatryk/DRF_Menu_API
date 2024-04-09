import pytest
from menu.infrastructure.repositories.memrepo import MemRepo
from menu.domain.entities.dish import Dish

@pytest.fixture
def dish_dicts():
    return [
    {
        "id" : 1,
        "name": "pizza",
        "description": "italish",
        "price": 2.99
    },
    {
        "id" : 2,
        "name": "hot-dog",
        "description": "americano",
        "price": 5.99
    },
    {
        "id" : 3,
        "name": "burger",
        "description": "amerciano",
        "price": 9.99
    },
    {
        "id" : 4,
        "name": "spaghetti",
        "description": "italish",
        "price": 7.29
    },
]


def test_repo_list(dish_dicts):
    repo = MemRepo(dish_dicts)
    dishes = [Dish.from_dict(d) for d in dish_dicts]
    assert repo.list() == dishes
