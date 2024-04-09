from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from menu.application.views import dish_list
import json
from menu.domain.entities.dish import Dish
from menu.application.serializer import DishSerializer

class DishListViewTestCase(TestCase):
    def setUp(self):
        self.dish1 = Dish.objects.create(name='Dish 1', description='Description 1', price=10.99)
        self.dish2 = Dish.objects.create(name='Dish 2', description='Description 2', price=15.99)
        
        self.client = APIClient()

    def test_dish_list_view(self):
        # Create a mock request
        # request = self.factory.get('/dishes/')

        # Mock repository with test data
        # test_dishes = [
        #     {'id': 1, 'name': 'pizza', 'description': 'italy', 'price': 10.99},
        #     {'id': 2, 'name': 'burger', 'description': 'american', 'price': 7.99},
        #     {'id': 3, 'name': 'spaghetti', 'description': 'italy', 'price': 5.99},
        #     {'id': 4, 'name': 'fries', 'description': 'american', 'price': 1.99}
        # ]

        # # Call the view function
        # response = dish_list(request)

        # # Check response status code
        # self.assertEqual(response.status_code, 200)

        # # Check response content
        # expected_content = json.dumps(test_dishes)
        # self.assertEqual(response.content.decode('utf-8'), expected_content)
        ################################################################
        url = reverse('dish-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Compare the serialized data with the response data
        expected_data = DishSerializer([self.dish1, self.dish2], many=True).data
        self.assertEqual(response.data, expected_data)


