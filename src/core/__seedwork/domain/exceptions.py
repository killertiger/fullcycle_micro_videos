from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.__seedwork.domain.validators import ErrorFields


class InvalidUuidException(Exception):
    def __init__(self, error='ID must be a valid UUID') -> None:
        super().__init__(error)


class ValidationException(Exception):
    pass


class BaseValidationException(Exception, ABC):
    error: 'ErrorFields'
    
    def __init__(self, error: 'ErrorFields' = None) -> None:
        if error is None:
            error = {}
        self.error = error
        super().__init__()
    
    def set_from_error(self, field: str, error: Exception):
        if error:
            self.error[field] = [error.args[0]]
            
    def __str__(self) -> str:
        return str(self.error)
    
    def __repr__(self) -> str:
        return str(self.error)

class EntityValidationException(BaseValidationException):
    pass

class SearchValidationException(BaseValidationException):
    pass

class LoadEntityException(BaseValidationException):
    pass

class NotFoundException(Exception):
    pass
