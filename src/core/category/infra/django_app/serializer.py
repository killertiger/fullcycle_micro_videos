from core.__seedwork.application.dto import PaginationOutput
from rest_framework import serializers, ISO_8601
from rest_framework.fields import empty


class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True, format=ISO_8601)


class PaginationSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    last_page = serializers.IntegerField()

class CategoryCollectionSerializer(serializers.ListSerializer):
    pagination: PaginationOutput
    child = CategorySerializer()
    many = False
    
    def __init__(self, pagination, **kwargs):
        self.pagination = pagination
        super().__init__(**kwargs)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'data': data,
            'meta': PaginationSerializer(self.pagination).data
        }
        
    @property
    def data(self):
        return self.to_representation(self.instance)
