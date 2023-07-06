from rest_framework.serializers import Serializer, ListSerializer


class SerializerCreateService:
    def __init__(self, serializer, validated_data, child_fields=None, fk_fields=None, m2m_fields=None):
        self._serializer = serializer
        self._validated_data = validated_data
        self._child_fields = child_fields or []
        self._fk_fields = fk_fields or []
        self._m2m_fields = m2m_fields or []
        for field in self._child_fields:
            self._validated_data.pop(field, None)

    @staticmethod
    def get_related_name_from_field_name(serializer_class, field_name):
        model = serializer_class.Meta.model
        for field in model._meta.get_fields():
            if hasattr(field, '_related_name') and field_name == field._related_name:
                return field.name

    @staticmethod
    def delete_related_instances_by_field_name(parent_instance, field_name):
        if hasattr(parent_instance, field_name):
            related_obj = getattr(parent_instance, field_name)
            if hasattr(related_obj, 'delete'):
                related_obj.delete()
            else:
                related_obj.all().delete()

    @staticmethod
    def get_serializer_class(field_type):
        if isinstance(field_type, ListSerializer):
            return field_type.child.__class__
        elif isinstance(field_type, Serializer):
            return field_type.__class__
        return None

    @staticmethod
    def get_data_from_context(context, field_name):
        request = context.get("request")
        data = context.get("raw_data", request.data).get(field_name, [])
        if not isinstance(data, list):
            return [data]
        return data

    def create_child_instances(self, parent_instance):
        context = self._serializer.context
        for field_name, field_type in self._serializer.fields.items():
            if field_name not in self._child_fields:
                continue

            serializer_class = self.get_serializer_class(field_type)
            if not serializer_class:
                continue

            self.delete_related_instances_by_field_name(parent_instance, field_name)
            raw_data_list = self.get_data_from_context(context, field_name)
            if raw_data_list == [None]:
                continue
            related_name = self.get_related_name_from_field_name(serializer_class, field_name)  # noqa
            for raw_data in raw_data_list:
                nested_context = {
                    'request': context.get("request"),
                    'raw_data': raw_data,
                }
                nested_serializer = serializer_class(data=raw_data, context=nested_context)
                nested_serializer.is_valid(raise_exception=True)
                nested_serializer.save(**{related_name: parent_instance})

    def create_fk_instances(self):
        context = self._serializer.context
        for field_name, field_type in self._serializer.fields.items():
            if field_name not in self._fk_fields:
                continue
            serializer_class = self.get_serializer_class(field_type)
            if not serializer_class:
                continue
            raw_data = self.get_data_from_context(context, field_name)
            if len(raw_data) < 1:
                continue
            raw_data = raw_data[0]
            nested_serializer = serializer_class(
                data=raw_data,
                context={
                    'request': self._serializer.context.get("request"),
                    'raw_data': raw_data,
                },
            )
            nested_serializer.is_valid(raise_exception=True)
            instance = nested_serializer.save()
            self._validated_data[field_name] = instance

    def create_m2m_instances(self, related_name: str, parent_instance):
        context = self._serializer.context
        for field_name, field_type in self._serializer.fields.items():
            if field_name not in self._m2m_fields:
                continue
            serializer_class = self.get_serializer_class(field_type)
            if not serializer_class:
                continue
            raw_data = self.get_data_from_context(context, field_name)
            if len(raw_data) < 1:
                continue

            related_manager = getattr(parent_instance, related_name)
            if related_manager.all().exists():
                self.delete_related_instances_by_field_name(parent_instance, field_name)

            nested_serializer = serializer_class(
                data=raw_data,
                context={
                    'request': self._serializer.context.get("request"),
                    'raw_data': raw_data,
                },
                many=True
            )
            nested_serializer.is_valid(raise_exception=True)
            nested_instances = nested_serializer.save()
            for instance in nested_instances:
                related_manager.add(instance)
            self._validated_data[field_name] = nested_instances
