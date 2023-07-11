from abc import ABC
import abc
from typing import TypeVar, Generic

Input = TypeVar('Input')
Output = TypeVar('Output')

class UseCase(Generic[Input, Output], ABC):
    @abc.abstractmethod
    def execute(self, input_param):
        raise NotImplementedError()