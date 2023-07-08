from rest_framework import viewsets, mixins

from test.models import News
from test.serialziers import NewsSerializer


class NewsApi(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def get_queryset(self):
        return News.objects.all()

    def get_serializer_class(self):
        return NewsSerializer
