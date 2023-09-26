from typing import TypeVar, Generic, List, Callable
from dataclasses import dataclass, field
from faker import Faker
from core.category.domain.entities import Category


T = TypeVar('T')

PropFactory = T | Callable[[int], T]


@dataclass
class CategoryFakerBuilder(Generic[T]):
    count_objs: int = 1

    __name: PropFactory[str] = field(
        default=lambda self, index: Faker().name(), init=False
    )
    __description: PropFactory[str | None] = field(
        default=lambda self, index: Faker().sentence(), init=False
    )
    __is_active: bool = field(default=lambda self, index: True, init=False)

    @staticmethod
    def a_category() -> 'CategoryFakerBuilder[Category]':
        return CategoryFakerBuilder[Category]()

    @staticmethod
    def the_categories(count: int) -> 'CategoryFakerBuilder[List[Category]]':
        return CategoryFakerBuilder[List[Category]](count)

    @staticmethod
    def a_movie():
        return CategoryFakerBuilder()

    # @staticmethod
    # def a_deactivate_category():
    #     return CategoryFakerBuilder()

    def with_name(self, value: PropFactory[str]):
        self.__name = value
        return self

    def with_description(self, value: PropFactory[str | None]):
        self.__description = value
        return self

    def activate(self):
        self.__is_active = True
        return self

    def deactivate(self):
        self.__is_active = False
        return self

    def build(self) -> T:
        categories = list(
            map(
                lambda index: Category(
                    name=self.__call_factory(self.__name, index),
                    description=self.__call_factory(self.__description, index),
                    is_active=self.__call_factory(self.__is_active, index),
                ),
                range(self.count_objs),
            )
        )

        return categories if self.count_objs > 1 else categories[0]

    @property
    def name(self):
        return self.__call_factory(self.__name, 0)

    @property
    def description(self):
        return self.__call_factory(self.__description, 0)

    @property
    def is_active(self):
        return self.__call_factory(self.__is_active, 0)

    def __call_factory(self, value: PropFactory[T], index: int) -> T:
        return value(index) if callable(value) else value
