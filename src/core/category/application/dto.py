from dataclasses import dataclass
from typing import Optional, TypeVar
from datetime import datetime

from core.category.domain.entities import Category


@dataclass(slots=True, frozen=True)
class CategoryOutput:
    id: str  # pylint: disable=invalid-name
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, category: Category):
        return cls(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        )

# TODO: Remove CategoryOutputMapper
Output = TypeVar('Output', bound=CategoryOutput)

# TODO: Remove CategoryOutputMapper
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
