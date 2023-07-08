from django.test import TestCase

from django.test.client import RequestFactory
from rest_framework import status
from rest_framework.response import Response
from test.api.o2o import RestaurantApi
from test.models import RestaurantDirector, Restaurant


class O2OCreateTestCase(TestCase):
    def setUp(self):
        request_factory = RequestFactory()
        create_o2o_request = request_factory.post(
            'api/restaurant/',
            data={
                "serves_hot_dogs": True,
                "serves_pizza": True,
                "director": {
                    'name': 'Cifra-k',
                }
            },
            content_type='application/json'
        )
        create_api = RestaurantApi.as_view(actions={'post': 'create'})
        self._response: Response = create_api(create_o2o_request)

    def get_director_from_response(self) -> dict:
        return self._response.data['director']

    def test_status_code(self):
        self.assertEqual(self._response.status_code, status.HTTP_201_CREATED)

    def test_response_contain_director(self):
        self.assertIn('director', self._response.data)

    def test_director_contain_id_in_response(self):
        director = self.get_director_from_response()
        self.assertIn('id', director)

    def test_director_created_in_db(self):
        director_id = self.get_director_from_response()['id']
        director_queryset = RestaurantDirector.objects.filter(pk=director_id)
        self.assertEqual(director_queryset.count(), 1)

    def test_director_related_with_restaurant(self):
        director_id = self.get_director_from_response()['id']
        restaurant_queryset = Restaurant.objects.filter(director__id=director_id)
        self.assertEqual(restaurant_queryset.count(), 1)

        restaurant_instance = restaurant_queryset.first()
        restaurant_response_id = self._response.data['id']
        self.assertEqual(restaurant_instance.pk, restaurant_response_id)
