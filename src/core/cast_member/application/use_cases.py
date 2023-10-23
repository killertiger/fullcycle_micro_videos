from dataclasses import dataclass
from core.__seedwork.application.use_cases import UseCase
from core.__seedwork.domain.exceptions import EntityValidationException
from core.cast_member.domain.entities import CastMember
from core.cast_member.domain.repositories import CastMemberRepository
from core.cast_member.domain.value_objects import CastMemberType

@dataclass(slots=True, frozen=True)
class CreateCastMemberUseCase(UseCase):
    
    cast_member_repo: CastMemberRepository
    
    def execute(self, request: 'Input') -> 'Output':
        cast_member_type, error_cast_member_type = CastMemberType.create(request.cast_member_type)
        
        try:
            cast_member = CastMember(
                name=request.name,
                cast_member_type=cast_member_type
            )
            self.cast_member_repo.insert(cast_member)
        except EntityValidationException as exception:
            exception.set_from_error('cast_member_type', error_cast_member_type)
            raise exception
        
    def __to_output(self, cast_member: CastMember) -> 'Output':
        return self.Output.from_entity(cast_member)
    
    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        cast_member_type: CastMemberType.TypeValues
    
    @dataclass(slots=True, frozen=True)
    class Output(CastMemberOutput):
        pass