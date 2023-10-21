from typing import Dict
from rest_framework import serializers
from core.__seedwork.domain.validators import ObjectField, StrictCharField, DRFValidator
from .entities import CastMemberType



class CastMemberRules(serializers.Serializer):
    name = StrictCharField(max_length=255)
    cast_member_type = ObjectField(instance_class=CastMemberType)
    created_at = serializers.DateTimeField(required=False)

class CastMemberValidator(DRFValidator):
    def validate(self, data: Dict):
        rules = CastMemberRules(data=data if data is not None else {})
        return super().validate(rules)
    
class CastMemberValidatorFactory:
    @staticmethod
    def create():
        return CastMemberValidator()