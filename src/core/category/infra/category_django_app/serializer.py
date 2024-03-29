from rest_framework import serializers
from rest_framework.fields import empty
from core.__seedwork.infra.django_app.serializers import CollectionSerializer, ResourceSerializer, ISO_8601


class CategorySerializer(ResourceSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True, format=ISO_8601)


class CategoryCollectionSerializer(CollectionSerializer):
    child = CategorySerializer()
