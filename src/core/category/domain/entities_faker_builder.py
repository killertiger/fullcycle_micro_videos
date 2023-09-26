from typing import TypeVar, Generic, List
from dataclasses import dataclass, field
from faker import Faker
from core.category.domain.entities import Category


T = TypeVar('T')

@dataclass
class CategoryFakerBuilder(Generic[T]):
    count_objs: int = 1
    
    name: str = field(default_factory=lambda: Faker().name(), init=False)
    description: str = field(default_factory=lambda: Faker().sentence(), init=False)
    is_active: bool = field(default=True, init=False)
    
    @staticmethod
    def a_category() -> 'CategoryFakerBuilder[Category]':
        return CategoryFakerBuilder[Category]()
    
    @staticmethod
    def the_categories(count: int) -> 'CategoryFakerBuilder[List[Category]]':
        return CategoryFakerBuilder[List[Category]](count)
        
    
    @staticmethod
    def a_movie():
        return CategoryFakerBuilder()
    
    @staticmethod
    def a_deactivate_category():
        return CategoryFakerBuilder()
    
    def with_name(self, name: str):
        self.name = name
        return self

    def activate(self):
        self.is_active = True
        return self
    
    def deactivate(self):
        self.is_active = False
        return self
    
    def build(self) -> T:
        categories = list(map(
            lambda value: Category(name=self.name, description=self.description, is_active=self.is_active),
            range(self.count_objs)
        ))
        
        return categories if self.count_objs > 1 else categories[0]