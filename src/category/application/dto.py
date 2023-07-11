from dataclasses import dataclass
from typing import Optional
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