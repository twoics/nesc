from rest_framework import serializers

from ..models.fk import News, Reporter
from nesc.nesc.service import SerializerCreateService


class ReporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporter
        fields = (
            'id',
            'first_name',
            'last_name',
        )


class NewsSerializer(serializers.ModelSerializer):
    reporter = ReporterSerializer(
        required=True
    )

    class Meta:
        model = News
        fields = (
            'id',
            'headline',
            'reporter'
        )

    def create(self, validated_data):
        service = SerializerCreateService(self, validated_data, fk_fields=['reporter'])
        service.create_fk_instances()
        return super().create(validated_data)
