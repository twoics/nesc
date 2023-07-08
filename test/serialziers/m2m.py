from rest_framework import serializers

from ..models.m2m import Article, Publication
from nesc.nesc.service import SerializerCreateService


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = (
            'id',
            'title',
        )


class ArticleSerializer(serializers.ModelSerializer):
    publications = PublicationSerializer(
        many=True
    )

    class Meta:
        model = Article
        fields = (
            'id',
            'headline',
            'publications',
        )

    def create(self, validated_data):
        validated_data.pop('publications')

        current_instance = super().create(validated_data)
        service = SerializerCreateService(self, validated_data, m2m_fields=['publications'])

        service.create_m2m_instances(
            related_name='publications',
            parent_instance=current_instance
        )
        return current_instance
