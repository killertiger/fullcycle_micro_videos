from typing import Callable, TypeVar, Generic, List, Any
from datetime import datetime
from dataclasses import dataclass, field
from core.cast_member.domain.entities import CastMember
from core.cast_member.domain.value_objects import CastMemberType
from faker import Faker
from core.__seedwork.domain.value_objects import UniqueEntityId

T = TypeVar('T')

PropOrFactory = T | Callable[[int], T]


@dataclass
class CastMemberFakerBuilder(Generic[T]):
    count_objs: int = 1

    __unique_entity_id: PropOrFactory[UniqueEntityId] = field(
        default=None, init=False)

    __name: PropOrFactory[str] = field(
        default=lambda self, index: Faker().name(), init=False)

    __cast_member_type: PropOrFactory[CastMemberType] = field(
        default=lambda self, index: CastMemberType.create_an_actor(), init=False
    )

    __created_at: PropOrFactory[datetime] = field(
        default=None, init=False
    )

    @staticmethod
    def an_actor() -> 'CastMemberFakerBuilder[CastMember]':
        return CastMemberFakerBuilder().with_type(CastMemberType.create_an_actor())

    @staticmethod
    def an_director() -> 'CastMemberFakerBuilder[CastMember]':
        return CastMemberFakerBuilder().with_type(CastMemberType.create_a_director())

    @staticmethod
    def the_actors(count: int) -> 'CastMemberFakerBuilder[List[CastMember]]':
        return CastMemberFakerBuilder(count).with_type(CastMemberType.create_an_actor())

    @staticmethod
    def the_directors(count: int) -> 'CastMemberFakerBuilder[List[CastMember]]':
        return CastMemberFakerBuilder(count).with_type(CastMemberType.create_a_director())

    def with_name(self, value: PropOrFactory[str]):
        self.__name = value
        return self

    def with_unique_entity_id(self, value: PropOrFactory[UniqueEntityId]):
        self.__unique_entity_id = value
        return self

    def with_cast_member_type(self, value: PropOrFactory[CastMemberType]):
        self.__cast_member_type = value
        return self

    def build(self) -> T:
        cast_members = list(
            map(
                lambda index: CastMember(
                    **{
                        **(
                            {
                                'unique_entity_id': self.__call_factory(
                                    self.__unique_entity_id, index
                                )
                            }
                            if self.__unique_entity_id is not None
                            else {}
                        ),
                        'name': self.__call_factory(self.__name, index),
                        'cast_member_type': self.__call_factory(self.__cast_member_type, index),
                        ** (
                            {
                                'created_at': self.__call_factory(
                                    self.__created_at, index
                                ),
                            }
                            if self.__created_at is not None
                            else {}
                        ),
                    }
                ),
                range(self.count_objs)
            )
        )

        return cast_members if self.count_objs > 1 else cast_members[0]

    @property
    def name(self) -> str:
        return self.__call_factory(self.__name, 0)

    # def cast_member_type(self) -> str:
    #     pass

    def created_at(self) -> datetime:
        value = self.__call_factory(self.created_at, 0)
        if value is None:
            raise Exception(
                'Prop created_at does not have a factory, use "with methods"'
            )

    def __call_factory(self, value: PropOrFactory[Any], index: int) -> Any:
        return value(index) if callable(value) else value

# TODO: Create invalid methods