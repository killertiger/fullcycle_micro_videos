from abc import ABC
import json
from dataclasses import dataclass, field, fields
import uuid
from __seedwork.domain.exceptions import InvalidUuidException

@dataclass(frozen=True)
class ValueObject(ABC):
    def __str__(self) -> str:
        fields_name = [field.name for field in fields(self)]
        return getattr(self, fields_name[0]) if len(fields_name) == 1 \
            else json.dumps({field_name: getattr(field_name) for field_name in fields_name})


@dataclass(frozen=True)
class UniqueEntityId(ValueObject):
    id: uuid.UUID = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    def __post_init__(self):
        id_value = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        object.__setattr__(self, 'id', id_value)
        self.__validate()

    def __validate(self):
        try:
            uuid.UUID(self.id)
        except ValueError as ex:
            raise InvalidUuidException() from ex
        
    # def __str__(self) -> str:
    #     return self.id