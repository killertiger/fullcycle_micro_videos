import unittest

from unittest.mock import patch

from category.application.use_cases import CreateCategoryUseCase
from category.domain.repositories import CategoryInMemoryRepository

class TestCreateCategoryUnitCaseUnit(unittest.TestCase):
    
    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository
    
    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)
        return super().setUp()
    
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