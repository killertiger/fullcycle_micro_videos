from typing import Any
from rest_framework import serializers

from __seedwork.domain.validators import DRFValidator

class CategoryRules(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)
    

class CategoryValidator(DRFValidator):
    def validate(self, data: Any):
        rules = CategoryRules(data=data)
        return super().validate(rules)
    
    
class CategoryValidatorFactory:
    @staticmethod
    def create():
        return CategoryValidator()