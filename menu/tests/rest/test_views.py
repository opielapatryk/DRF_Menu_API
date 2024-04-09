import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menu.settings")

import django
django.setup()
import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from application.views import DishView

class DishViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_all_dishes(self):
        request = self.factory.get('/dishes/')
        view = DishView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4) 

    def test_get_single_dish(self):
        request = self.factory.get('/dishes/1/')
        view = DishView.as_view()
        response = view(request, pk=1)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data[0], dict)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], 'pizza')

    def test_post_dish(self):
        request_data = {
            "id":5,
            "name": "sushi",
            "description": "japanese",
            "price": 12.99
        }
        request = self.factory.post('/dishes/', data=json.dumps(request_data), content_type='application/json')
        view = DishView.as_view()
        response = view(request)
        
        print(response.data)

        self.assertEqual(response.status_code, 201)  
        self.assertEqual(response.data[4]['name'], 'sushi')
        self.assertEqual(response.data[4]['description'], 'japanese')
        self.assertEqual(response.data[4]['price'], 12.99)

    def test_delete_dish(self):
        request = self.factory.delete('/dishes/5/')
        view = DishView.as_view()
        response = view(request, pk=5)
        
        self.assertEqual(response.status_code, 204)  

    def test_put_dish(self):
        request_data = {
            "id":1,
            "name": "updated dish",
            "description": "updated description",
            "price": 15.99
        }
        request = self.factory.put('/dishes/', data=json.dumps(request_data), content_type='application/json')
        view = DishView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data[0]['name'], 'updated dish')
        self.assertEqual(response.data[0]['price'], 15.99)
