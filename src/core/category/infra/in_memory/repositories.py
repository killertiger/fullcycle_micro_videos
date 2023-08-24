from typing import List, Any
from core.__seedwork.domain.repositories import InMemorySearchableRepository
from core.category.domain.entities import Category

from core.category.domain.repositories import CategoryRepository


class CategoryInMemoryRepository(CategoryRepository, InMemorySearchableRepository):
    sortable_fields: List[str] = ['created_at', 'name']

    def _apply_filter(self, items: List[Category], filter_param: Any | None) -> List[Category]:
        if filter_param:
            items = filter(lambda i: filter_param.lower()
                           in i.name.lower(), items)
        return list(items)

    def _apply_sort(self, items: List, sort: str | None, sort_dir: str | None) -> List:
        if not sort:
            sort = 'created_at'
            sort_dir = 'desc'

        return super()._apply_sort(items, sort, sort_dir)
