from typing import TYPE_CHECKING
from core.__seedwork.domain.exceptions import EntityValidationException, LoadEntityException
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.cast_member.domain.entities import CastMember

from core.cast_member.domain.value_objects import CastMemberType


if TYPE_CHECKING:
    from .models import CastMemberModel
    
class CastMemberModelMapper:
    
    @staticmethod
    def to_entity(model: 'CastMemberModel') -> CastMember:
        cast_member_type, error_cast_member_type = CastMemberType.create(model.type)
        
        try:
            return CastMember(
                unique_entity_id=UniqueEntityId(str(model.id)),
                name=model.name,
                cast_member_type=model.cast_member_type,
                created_at=model.created_at,
            )
        except EntityValidationException as exception:
            exception.set_from_error('cast_member_type', error_cast_member_type)
            raise LoadEntityException(exception.error) from exception
        
    @staticmethod
    def to_model(entity: CastMember) -> 'CastMemberModel':
        from .models import CastMemberModel
        return CastMemberModel(**entity.to_dict())