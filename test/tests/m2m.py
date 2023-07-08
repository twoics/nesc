from django.test import TestCase
from rest_framework.response import Response
from rest_framework import status

from test.api.m2m import ArticleApi
from django.test.client import RequestFactory
from test.models.m2m import Publication, Article


class M2MCreateTestCase(TestCase):
    def setUp(self):
        request_factory = RequestFactory()
        create_m2m_request = request_factory.post(
            'api/article/',
            data={
                "headline": "Заголовок статьи",
                "publications": [
                    {
                        "title": "Первая публикация"
                    },
                    {
                        "title": "Вторая публикация"
                    }
                ]
            },
            content_type='application/json'
        )
        create_api = ArticleApi.as_view(actions={'post': 'create'})
        self._response: Response = create_api(create_m2m_request)

    def get_publications_pk_from_response(self) -> tuple:
        publication_response = self._response.data.get('publications')
        return publication_response[0]['id'], publication_response[1]['id']

    def test_response_status(self):
        self.assertEqual(self._response.status_code, status.HTTP_201_CREATED)

    def test_response_contain_publications(self):
        self.assertIn('publications', self._response.data)

    def test_count_publication(self):
        publication_response = self._response.data.get('publications')
        self.assertEqual(len(publication_response), 2)

    def test_publications_response_contains_id(self):
        publication_response = self._response.data.get('publications')
        self.assertIn('id', publication_response[0])
        self.assertIn('id', publication_response[1])

    def test_publications_created(self):
        first_publication_pk, second_publication_pk = self.get_publications_pk_from_response()

        publication_queryset = Publication.objects.filter(pk__in=[first_publication_pk, second_publication_pk])
        self.assertEqual(publication_queryset.count(), 2)

    def test_publication_related_with_article(self):
        first_publication_pk, second_publication_pk = self.get_publications_pk_from_response()

        first_publication_related_article = Article.objects.filter(publications__id=first_publication_pk)
        second_publication_related_article = Article.objects.filter(publications__id=first_publication_pk)
        self.assertEqual(first_publication_related_article.count(), 1)
        self.assertEqual(second_publication_related_article.count(), 1)

        self.assertEqual(
            first_publication_related_article.first().pk,
            second_publication_related_article.first().pk
        )
