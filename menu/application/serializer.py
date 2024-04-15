from rest_framework import serializers
from domain.entities.dish import Dish

class DishSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()

    def create(self, validated_data):
        return Dish.from_dict(validated_data)
    
