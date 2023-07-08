from rest_framework import viewsets, mixins

from test.models import Restaurant
from test.serialziers import RestaurantSerializer


class RestaurantApi(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def get_queryset(self):
        return Restaurant.objects.all()

    def get_serializer_class(self):
        return RestaurantSerializer
