import datetime
from typing import Optional
from dataclasses import dataclass, field
from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.exceptions import EntityValidationException
from core.cast_member.domain.validators import CastMemberValidatorFactory
from core.cast_member.domain.value_objects import CastMemberType


@dataclass(kw_only=True, frozen=True, slots=True)
class CastMember(Entity):
    name: str
    cast_member_type: CastMemberType
    created_at: Optional[datetime.datetime] = field(
        default_factory= lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    
    def __post_init__(self):
        if not self.created_at:
            self._set('created_at', datetime.datetime.now(datetime.timezone.utc))
        self.validate()
        
    def update(self, name: str, cast_member_type: CastMemberType):
        self._set('name', name)
        self._set('cast_member_type', cast_member_type)
        self.validate()
    
    def validate(self):
        validator = CastMemberValidatorFactory.create()
        # is_valid = validator.validate(self.to_dict())
        is_valid = validator.validate({
            'name': self.name,
            'cast_member_type': self.cast_member_type,
        })
        if not is_valid:
            raise EntityValidationException(validator.errors)
    
    def to_dict(self):
        data = super(CastMember, self).to_dict()
        data[cast_member_type] = self.cast_member_type.value.value
        return data
    
    @staticmethod
    def fake():
        from .entities_faker_builder import CastMemberFakerBuilder
        return CastMemberFakerBuilder