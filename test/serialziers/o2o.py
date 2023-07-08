from rest_framework import serializers

from ..models.o2o import Place, Restaurant
from nesc.nesc.service import SerializerCreateService


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = (
            'id',
            'name',
            'address',
        )


class RestaurantSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(
        required=True
    )

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'place',
            'serves_hot_dogs'
            'serves_pizza'
        )

    def create(self, validated_data):
        data_without_place = validated_data.copy()
        data_without_place.pop('place')
        restaurant = super().create(data_without_place)

        service = SerializerCreateService(self, validated_data, child_fields=['place'])
        service.create_child_instances(restaurant)
        return restaurant
