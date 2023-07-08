from django.test import TestCase
from django.test.client import RequestFactory
from rest_framework import status
from rest_framework.response import Response

from test.api.fk import NewsApi
from test.models.fk import News, Reporter


class FKCreateTestCase(TestCase):
    def setUp(self):
        request_factory = RequestFactory()
        create_fk_request = request_factory.post(
            'api/news/',
            data={
                "headline": "Заголовок статьи",
                "reporter": {
                    'first_name': 'Имя',
                    'last_name': 'Фамилия'
                }
            },
            content_type='application/json'
        )
        create_api = NewsApi.as_view(actions={'post': 'create'})
        self._response: Response = create_api(create_fk_request)

    def get_reporter_from_response(self) -> dict:
        data = self._response.data
        return data['reporter']

    def test_response_status_code(self):
        self.assertEqual(self._response.status_code, status.HTTP_201_CREATED)

    def test_reporter_exists_in_response(self):
        data = self._response.data
        self.assertIn("reporter", data)

    def test_reporter_response_contain_id(self):
        reporter_response = self.get_reporter_from_response()
        self.assertIn("id", reporter_response)

    def test_reporter_created_in_db(self):
        reporter_response_id = self.get_reporter_from_response()['id']
        reporter_queryset = Reporter.objects.filter(pk=reporter_response_id)
        self.assertEqual(reporter_queryset.count(), 1)

    def test_reporter_related_with_news(self):
        reporter_response_id = self.get_reporter_from_response()['id']
        news_queryset = News.objects.filter(
            reporter__id=reporter_response_id
        )
        self.assertEqual(news_queryset.count(), 1)
