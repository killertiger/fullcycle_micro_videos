from typing import Union, Literal
from enum import Enum
from dataclasses import dataclass, field, InitVar
from core.__seedwork.domain.utils import Either
from core.__seedwork.domain.value_objects import ValueObject
from .exceptions import InvalidCastMemberTypeException


@dataclass(frozen=True, slots=True)
class CastMemberType(ValueObject):
    value: 'Type' = field(init=False)
    init_value: InitVar[Union['Type', str]]
    
    class Type(Enum):
        DIRECTOR = 1
        ACTOR = 2
        
    TypeValues = Literal[1, 2]
    
    def __post_init__(self, init_value: Union['Type', str]):
        value = self.__validate(init_value)
        object.__setattr__(self, 'value', value)
        
    def __validate(self, value: Union['Type', str]):
        if isinstance(value, CastMemberType.Type):
            return value
        
        try:
            return CastMemberType.Type(value)
        except ValueError as ex:
            raise InvalidCastMemberTypeException(value) from ex
        
    @staticmethod
    def create(value: Union['Type', str]):
        return Either.safe(lambda: CastMemberType(value))
    
    @staticmethod
    def create_an_actor():
        return CastMemberType(CastMemberType.Type.ACTOR)
    
    @staticmethod
    def create_a_director():
        return CastMemberType(CastMemberType.Type.DIRECTOR)
