from dataclasses import dataclass
from typing import Optional
from __seedwork.application.use_cases import UseCase
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository
from .dto import CategoryOutput, CategoryOutputMapper

@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        category = Category(
            name=input_param.name,
            description=input_param.description,
            is_active=input_param.is_active
        )
        
        self.category_repo.insert(category)
        
        return self.__to_output(category)

    def __to_output(self, category: Category):
        return CategoryOutputMapper.to_output(category)
    
    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = Category.get_field('description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class GetCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        category = self.category_repo.find_by_id(input_param.id)
        
        return self.__to_output(category)
        
    def __to_output(self, category: Category):
        return CategoryOutputMapper.to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass

# Learning:
# SOLID - S = Single Responsibility
# The class should have only one responsibility
# The class should have only one reason to be changed
# Due to that, it's better to have one class for each operation, otherwise,
# we would have many reasons to change this class