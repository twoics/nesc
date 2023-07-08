from rest_framework import viewsets, mixins

from test.models import Article
from test.serialziers import ArticleSerializer


class ArticleApi(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def get_queryset(self):
        return Article.objects.all()

    def get_serializer_class(self):
        return ArticleSerializer
