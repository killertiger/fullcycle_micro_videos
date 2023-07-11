from typing import Optional
import unittest
from unittest.mock import patch

from category.application.use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase
    )
from category.application.dto import CategoryOutput
from category.domain.repositories import CategoryInMemoryRepository
from category.domain.entities import Category
from __seedwork.domain.exceptions import NotFoundException

class TestCreateCategoryUnitCaseUnit(unittest.TestCase):
    
    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository
    
    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)
        return super().setUp()
    
    def test_input(self) -> None:
        self.assertEqual(
            CreateCategoryUseCase.Input.__annotations__, {
                'name': str,
                'description': Optional[str],
                'is_active': Optional[bool]
            }
        )
        
        description_field = CreateCategoryUseCase.Input.__dataclass_fields__['description']
        self.assertEqual(description_field.default, Category.get_field('description').default)
        
        is_active_field = CreateCategoryUseCase.Input.__dataclass_fields__['is_active']
        self.assertEqual(is_active_field.default, Category.get_field('is_active').default)
        
    def test_output(self) -> None:
        self.assertTrue(
            issubclass(
                CreateCategoryUseCase.Output,
                CategoryOutput
            )
        )
    
    def test_execute(self) -> None:
        with patch.object(self.category_repo, 'insert', wraps=self.category_repo.insert) as spy_insert:
            input_param = CreateCategoryUseCase.Input(name='Movie')
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id=self.category_repo.items[0].id,
                name='Movie',
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at
            ))
            
            input_param = CreateCategoryUseCase.Input(name='Movie 2', description='test description 2', is_active=False)
            output = self.use_case.execute(input_param)
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id=self.category_repo.items[1].id,
                name='Movie 2',
                description='test description 2',
                is_active=False,
                created_at=self.category_repo.items[1].created_at
            ))
        
            input_param = CreateCategoryUseCase.Input(name='Movie 3', description='test description 3', is_active=True)
            output = self.use_case.execute(input_param)
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id=self.category_repo.items[2].id,
                name='Movie 3',
                description='test description 3',
                is_active=True,
                created_at=self.category_repo.items[2].created_at
            ))
            
class TestGetCategoryUnitCaseUnit(unittest.TestCase):
    
    use_case: GetCategoryUseCase
    category_repo: CategoryInMemoryRepository
    
    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = GetCategoryUseCase(self.category_repo)
        return super().setUp()
    
    def test_input(self) -> None:
        self.assertEqual(GetCategoryUseCase.Input.__annotations__, {
            'id': str,
        })
    
    def test_throws_exception_when_category_not_found(self):
        input_param = GetCategoryUseCase.Input(id='fake id')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(assert_error.exception.args[0], "Entity not found using ID 'fake id'")
    
    def test_output(self) -> None:
        self.assertTrue(
            issubclass(
                GetCategoryUseCase.Output,
                CategoryOutput
            )
        )
    
    def test_execute(self) -> None:
        category = Category(name='Movie')
        self.category_repo.items = [category]
        
        with patch.object(self.category_repo, 'find_by_id', wraps=self.category_repo.find_by_id) as spy_insert:
            input_param = GetCategoryUseCase.Input(id=category.id)
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output, GetCategoryUseCase.Output(
                id=self.category_repo.items[0].id,
                name='Movie',
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at
            ))