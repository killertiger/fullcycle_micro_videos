from dataclasses import dataclass, field
from faker import Faker
from core.category.domain.entities import Category

@dataclass
class CategoryFakerBuilder:
    name: str = field(default_factory=lambda: Faker().name(), init=False)
    description: str = field(default_factory=lambda: Faker().sentence(), init=False)
    is_active: bool = field(default=True, init=False)
    
    @staticmethod
    def a_category():
        return CategoryFakerBuilder()
    
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
    
    def build(self):
        return Category(name=self.name, description=self.description, is_active=self.is_active)