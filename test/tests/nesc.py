from django.test import TestCase
from test.serialziers.m2m import PublicationSerializer, ArticleSerializer


class NescTestCase(TestCase):
    def test_m2m_create(self):
        serializer = ArticleSerializer(data={
            'headline': 'Название',
            'publications': [
                {
                    'title': 'Публикация 1'
                },
                {
                    'title': 'Публикация 2'
                }
            ]
        })
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        print(instance)