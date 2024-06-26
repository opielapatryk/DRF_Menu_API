from rest_framework.views import APIView
from rest_framework.response import Response
from application.serializer import DishSerializer
from infrastructure.repositories.memrepo import MemRepo
from infrastructure.repositories.postgrerepo import PostgresRepo
from infrastructure.repositories.mongorepo import MongoRepo
from domain.use_cases.dish_list_use_case import dish_list_use_case
from domain.use_cases.dish_post_use_case import dish_post_use_case
from domain.use_cases.dish_get_use_case import dish_get_use_case
from domain.use_cases.dish_put_use_case import dish_put_use_case
from domain.use_cases.dish_patch_use_case import dish_patch_use_case
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

mongo_configuration = {
    "MONGODB_HOSTNAME": 'db',
    "MONGODB_PORT": 27017,
    "MONGODB_USER": 'root',
    "MONGODB_PASSWORD": 'mongodb',
    "APPLICATION_DB": 'restaurant',
}

postgres_configuration = {
    "POSTGRES_USER": 'postgres',
    "POSTGRES_PASSWORD": 'postgres',
    "POSTGRES_HOSTNAME": 'db',
    "POSTGRES_PORT": 5432,
    "APPLICATION_DB": 'restaurant',
}

class Root(APIView):
    def get(self,request):
        return Response({'dishes': 'http://localhost:8000/api/v1/dishes/'})

class DishView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            dish_id = pk
            repo = PostgresRepo(postgres_configuration)
            dish = dish_get_use_case(repo, dish_id)
            
            if dish:
                serializer = DishSerializer(dish).data
                return Response(serializer)
            else:
                return Response({"message": "Dish not found"}, status=status.HTTP_404_NOT_FOUND)

        repo = PostgresRepo(postgres_configuration)
        results = dish_list_use_case(repo)
        serializer = DishSerializer(results, many=True).data

        # Filtering options
        description = request.query_params.get('description')
        min_price = float(request.query_params.get('min_price', 0))
        max_price = float(request.query_params.get('max_price', float('inf')))

        # Apply filters
        filtered_dishes = filter(lambda p: p['price'] >= min_price and p['price'] <= max_price, serializer)

        if description:
            filtered_dishes = filter(lambda p: p['description'] == description, filtered_dishes)


        # Sorting parameters
        sort_by = request.query_params.get('sort_by', 'id')
        sort_order = request.query_params.get('sort_order', 'asc')
        sorted_dishes = sorted(filtered_dishes, key=lambda p: p[sort_by], reverse=sort_order.lower() == 'desc')

        # Pagination parameters
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))

        # Paginate the results
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_dishes = sorted_dishes[start_index:end_index]

        return Response(paginated_dishes)
    
    def post(self, request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            repo = PostgresRepo(postgres_configuration)
            new_dish_data = serializer.validated_data
            try:
                new_dish = dish_post_use_case(repo, new_dish_data)
                serializer = DishSerializer(new_dish,many=True).data
                return Response(serializer, status=status.HTTP_201_CREATED)
            except:
                return Response({"message": "Dish already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk=None):
        if pk is not None:
            dish_id = pk
            serializer = DishSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                repo = PostgresRepo(postgres_configuration)
                updated_dish_list = dish_patch_use_case(repo, serializer.validated_data,dish_id)
                serializer = DishSerializer(updated_dish_list, many=True).data
                if serializer:
                    return Response(serializer, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def put(self, request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            repo = PostgresRepo(postgres_configuration)
            updated_dish_list = dish_put_use_case(repo, serializer.validated_data)
            serializer = DishSerializer(updated_dish_list, many=True).data
            if serializer:
                return Response(serializer, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            dish_id = pk
            repo = PostgresRepo(postgres_configuration)
            dish = dish_delete_use_case(repo, dish_id)
            
            if dish:
                serializer = DishSerializer(dish, many=True).data
                return Response(serializer, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Dish not found"}, status=status.HTTP_404_NOT_FOUND)
            