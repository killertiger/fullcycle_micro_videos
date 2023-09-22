from rest_framework import serializers
from core.__seedwork.application.dto import PaginationOutput


class UUIDSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class PaginationSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    last_page = serializers.IntegerField()


class CollectionSerializer(serializers.ListSerializer):
    pagination: PaginationOutput
    many = False

    def __init__(self, instance: PaginationOutput = None, **kwargs):
        if isinstance(instance, PaginationOutput):
            kwargs['instance'] = instance.items
            self.pagination = instance
        else:
            raise TypeError('instance must be a PaginationOutput')

        super().__init__(**kwargs)

    def to_representation(self, data):
        data = super().to_representation(data)
        return {'data': data, 'meta': PaginationSerializer(self.pagination).data}

    @property
    def data(self):
        return self.to_representation(self.instance)
