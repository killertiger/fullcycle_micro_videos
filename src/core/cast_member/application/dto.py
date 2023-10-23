from dataclasses import dataclass
from datetime import datetime
from core.cast_member.domain.entities import CastMember, CastMemberType


@dataclass(frozen=True, slots=True)
class CastMemberOutput:
    id: str
    name: str
    cast_member_type: CastMemberType.TypeValues
    created_at: datetime
    
    @classmethod
    def from_entity(cls, cast_member: CastMember):
        return cls(
            id=cast_member.id,
            name=cast_member.name,
            cast_member_type=cast_member.cast_member_type,
            created_at=cast_member.created_at
        )
    