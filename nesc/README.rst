=====
NESCS
=====
    ``NESTED SERIALIZER CREATE SERVICE``

Installation
------------
Установка через PyPi::

    pip install nescs

Description
-----------
Данная библиотека позволяет автоматически создавать объекты во
вложенных сериализаторах.
Работу по созданию вложенных объектов берет на себя сервис -
``SerializerCreateService``.
Он поддерживает создание объектов в случаях

1. Many to many
2. One to one
3. Foreign key


Examples
--------
Ниже расположено несколько примеров использования библиотеки на
различных вариантах связи между моделями

Many to many case
~~~~~~~~~~~~~~~~~
Для создание объектов с отношением **m2m** используется метод ``create_m2m_instances``

Пример кода для случая **m2m**::

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
            service = SerializerCreateService(self, validated_data, m2m_fields=['publications'])
            current_instance = super().create(validated_data)

            service.create_m2m_instances(
                parent_instance=current_instance
            )
            return current_instance

One to one case
~~~~~~~~~~~~~~~~~
Для создание объектов с отношением **o2o** используется метод ``create_child_instances``

Пример кода для случая **o2o**::

    class RestaurantDirectorSerializer(serializers.ModelSerializer):
        class Meta:
            model = RestaurantDirector
            fields = (
                'id',
                'name',
            )

    class RestaurantSerializer(serializers.ModelSerializer):
        director = RestaurantDirectorSerializer(
            required=True
        )

        class Meta:
            model = Restaurant
            fields = (
                'id',
                'serves_hot_dogs',
                'serves_pizza',
                'director',
            )

        def create(self, validated_data):
            service = SerializerCreateService(
                self,
                validated_data,
                child_fields=['director']
            )
            restaurant = super().create(validated_data)

            service.create_child_instances(restaurant)
            return restaurant

Foreign key case
~~~~~~~~~~~~~~~~~
Для создание объектов с отношением **fk** используется метод ``create_fk_instances``

Пример кода для случая **fk**::

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


Feature
-------
    Полезные фичи

- При **инициализации** сервиса, он автоматически удаляет из ``validated_data`` поля указанные в ``m2m_fields`` и ``child_fields`` Поэтому вам ненужно вручную очищать ``validated_data`` от вложенных объектов для создания родительского объекта. Просто вызовите создание родительского объекта после инициализации сервиса. (Полезно для **o2o** и **m2m**)

- После вызова одного из методов создания вложенных объектов, в ``validated_data`` будут помещены экземпляры созданных объектов
