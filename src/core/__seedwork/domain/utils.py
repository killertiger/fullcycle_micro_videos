from collections.abc import Iterable
from typing import Callable, Tuple, TypeVar

Ok = TypeVar('Ok')
Error = TypeVar('Error')

class Either(Tuple[Ok, Error]):
    
    def __new__(cls, ok: Ok, error: Error):
        return super().__new__(cls, (ok, error))
    
    @property
    def ok(self) -> Ok:
        return self[0]
    
    @property
    def error(self) -> Error:
        return self[1]
    
    @property
    def is_ok(self) -> bool:
        return self[0] is not None
    
    @property
    def is_error(self) -> bool:
        return self[1] is not None
    
    @staticmethod
    def of(ok: Ok) -> 'Either[Ok, None]':
        return Either.from_ok(ok)
    
    @staticmethod
    def from_ok(ok: Ok) -> 'Either[Ok, None]':
        return Either(ok, None)
    
    @staticmethod
    def fail(error: Error) -> 'Either[None, Error]':
        return Either(None, error)
    
    @staticmethod
    def safe(fn: Callable[[], Ok]) -> 'Either[Ok, Error]':
        try:
            return Either.of(fn())
        except Exception as ex:
            return Either.fail(ex)
    
    def __repr__(self) -> str:
        return f'Either({self[0]}, {self[1]})'