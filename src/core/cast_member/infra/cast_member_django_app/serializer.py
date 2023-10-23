from rest_framework import serializers 
from core.__seedwork.infra.django_app.serializers import (ResourceSerializer, ISO_8601)
from core.cast_member.domain.entities import CastMemberType

class CastMemberSerializer(ResourceSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    cast_member_type = serializers.ChoiceField(
        choices=[x.value for x in CastMemberType.Type]
    )
    created_at = serializers.DateTimeField(read_only=True, format=ISO_8601)
    
class CastMemberCollectionSerializer(ResourceSerializer):
    child = CastMemberSerializer()