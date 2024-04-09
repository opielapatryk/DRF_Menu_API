from rest_framework.views import APIView
from rest_framework.response import Response
from application.serializer import DishSerializer
from infrastructure.repositories.memrepo import MemRepo
from domain.use_cases.dish_list_use_case import dish_list_use_case
from domain.use_cases.dish_post_use_case import dish_post_use_case
from domain.use_cases.dish_get_use_case import dish_get_use_case
from domain.use_cases.dish_put_use_case import dish_put_use_case
from domain.use_cases.dish_del_use_case import dish_delete_use_case
from rest_framework import status

dishes = [
    {
    "id" : 1,
    "name": "pizza",
    "description": "italy",
    "price": 10.99
    },
    {
    "id" : 2,
    "name": "burger",
    "description": "american",
    "price": 7.99
    },
    {
    "id" : 3,
    "name": "spaghetti",
    "description": "italy",
    "price": 5.99
    },
    {
    "id" : 4,
    "name": "fries",
    "description": "american",
    "price": 1.99
    },
]

class DishView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            dish_id = pk
            repo = MemRepo(dishes) 
            dish = dish_get_use_case(repo, dish_id)
            
            if dish:
                serializer = DishSerializer(dish, many=True).data
                return Response(serializer)
            else:
                return Response({"message": "Dish not found"}, status=status.HTTP_404_NOT_FOUND)

        repo = MemRepo(dishes) 
        results = dish_list_use_case(repo)
        serializer = DishSerializer(results, many=True).data
        return Response(serializer)
    
    def post(self, request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            repo = MemRepo(dishes)
            new_dish_list = dish_post_use_case(repo, serializer.validated_data)
            serializer = DishSerializer(new_dish_list, many=True).data
            return Response(serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            repo = MemRepo(dishes)
            updated_dish_list = dish_put_use_case(repo, serializer.validated_data)
            serializer = DishSerializer(updated_dish_list, many=True).data
            return Response(serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            dish_id = pk
            repo = MemRepo(dishes) 
            dish = dish_delete_use_case(repo, dish_id)
            
            if dish:
                serializer = DishSerializer(dish, many=True).data
                return Response(serializer, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Dish not found"}, status=status.HTTP_404_NOT_FOUND)