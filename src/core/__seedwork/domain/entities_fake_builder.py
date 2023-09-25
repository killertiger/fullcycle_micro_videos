from dataclasses import dataclass, Field
from core.category.domain.entities import Category

@dataclass
class CategoryFakerBuilder:
    name: str = Field(default='Movie', init=False)
    is_active: bool = Field(default=True, init=False)
    
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
        Category(name=self.name, is_active=self.is_active)