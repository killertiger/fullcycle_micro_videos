from typing import Any, Dict, List, Generic, TypeVar
from dataclasses import dataclass
from abc import ABC, abstractmethod
from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, BooleanField, Field, empty
from django.conf import settings

from .exceptions import ValidationException

if not settings.configured:
    settings.configure(USE_I18N=False)


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value, prop) -> 'ValidatorRules':
        return ValidatorRules(value, prop)

    def required(self) -> 'ValidatorRules':
        if self.value is None or self.value == "":
            raise ValidationException(f'The {self.prop} is required')
        return self

    def string(self) -> 'ValidatorRules':
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f'The {self.prop} must be a string')
        return self

    def max_length(self, max_length: int) -> 'ValidatorRules':
        if self.value is not None and len(self.value) > max_length:
            raise ValidationException(
                f'The {self.prop} must be less than {max_length} characters')
        return self

    def boolean(self) -> 'ValidatorRules':
        if self.value is not None and self.value is not True and self.value is not False:
            raise ValidationException(f'The {self.prop} must be a boolean')
        return self


ErrorFields = Dict[str, List[str]]

PropsValidated = TypeVar('PropsValidated')


@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):
    errors: ErrorFields = None
    validated_data: PropsValidated = None

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


class DRFValidator(ValidatorFieldsInterface[PropsValidated], ABC):  # pylint: disable=too-few-public-methods
    def validate(self, data: Serializer) -> bool:
        serializer = data

        if serializer.is_valid():
            self.validated_data = serializer.validated_data
            return True

        self.errors = {
            field: [str(_error) for _error in _errors]
            for field, _errors in serializer.errors.items()
        }
        return False


class StrictCharField(CharField):
    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('invalid')

        return super().to_internal_value(data)


class StrictBooleanField(BooleanField):
    def to_internal_value(self, data):  # pylint: disable=inconsistent-return-statements
        try:
            if data is True:
                return True
            if data is False:
                return False
            if data is None and self.allow_null:
                return None
        except TypeError:
            pass
        self.fail('invalid', input=data)

class ObjectField(Field):
    default_error_message = {
        # 'invalid': _('Not a instance of {instance_name}'),
        'invalid': 'Not a instance of {instance_name}', # TODO : Fix this
    }
    
    def __init__(self, instance_class, **kwargs):
        self.instance_class = instance_class
        if self.instance_class is None:
            raise TypeError('The `instance_class` argument is required.')
        super().__init__(**kwargs)
        
    def run_validation(self, data=empty):
        super().run_validation(data)
        if self.required and not self.allow_null and not isinstance(data, self.instance_class):
            self.fail('invalid', instance_name=self.instance_class.__name__)
        return data
    
    def to_internal_value(self, data):
        return data
    
    def to_representation(self, value):
        return value