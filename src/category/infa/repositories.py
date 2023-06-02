from category.domain.repositories import CategoryRepository
from __seedwork.domain.repositories import InMemoryRepository


class CategoryInMemoryRepository(CategoryRepository, InMemoryRepository):
    pass