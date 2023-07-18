from dataclasses import dataclass
from typing import Optional, TypeVar
from datetime import datetime

from category.domain.entities import Category

@dataclass(slots=True, frozen=True)
class CategoryOutput:
    id: str
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    
    
class CategoryOutputMapper:
    
    @staticmethod
    def to_output(category: Category) -> CategoryOutput:
        return CategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        )
        
Output = TypeVar('Output', bound=CategoryOutput)

@dataclass(slots=True, frozen=True)
class CategoryOutputMapper:
    output_child: Optional[Output] = CategoryOutput
    
    @staticmethod
    def from_child(output_child: Output):
        return CategoryOutputMapper(output_child)
    
    @staticmethod
    def without_child():
        return CategoryOutputMapper()
    
    def to_output(self, category: Category) -> CategoryOutput:
        return self.output_child(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        )
    