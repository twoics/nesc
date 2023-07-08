from rest_framework import serializers

from ..models.o2o import RestaurantDirector, Restaurant
from nesc.nesc.service import SerializerCreateService


class RestaurantDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDirector
        fields = (
            'id',
            'name',
        )


class RestaurantSerializer(serializers.ModelSerializer):
    director = RestaurantDirectorSerializer(
        required=True
    )

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'serves_hot_dogs',
            'serves_pizza',
            'director',
        )

    def create(self, validated_data):
        service = SerializerCreateService(
            self,
            validated_data,
            child_fields=['director']
        )
        restaurant = super().create(validated_data)

        service.create_child_instances(restaurant)
        return restaurant
