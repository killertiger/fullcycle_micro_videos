import unittest
import pytest
from core.category.application.use_cases import (
    CreateCategoryUseCase,
)
from core.category.infra.django_app.repositories import CategoryDjangoRepository

@pytest.mark.django_db
class TestCreateCategoryUseInt(unittest.TestCase):
    
    use_case: CreateCategoryUseCase
    repo: CategoryDjangoRepository
    
    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()
        self.use_case = CreateCategoryUseCase(self.repo)
        
    def test_execute(self):
        input_param = CreateCategoryUseCase.Input(name='Movie')
        output = self.use_case.execute(input_param)
        
        entity = self.repo.find_by_id(output.id)
        
        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=entity.id,
            name='Movie',
            description=None,
            is_active=True,
            created_at=entity.created_at
        ))
        
        self.assertEqual(entity.name, 'Movie')
        self.assertIsNone(entity.description)
        self.assertTrue(entity.is_active)
        
        input_param = CreateCategoryUseCase.Input(name='Movie2', description='some description')
        
        output = self.use_case.execute(input_param)
        entity = self.repo.find_by_id(output.id)
        
        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=entity.id,
            name='Movie2',
            description='some description',
            is_active=True,
            created_at=entity.created_at
        ))
        self.assertEqual(entity.name, 'Movie2')
        self.assertEqual(entity.description, 'some description')
        self.assertTrue(entity.is_active)
        
        input_param = CreateCategoryUseCase.Input(name='Movie3', description='some description3')
        
        output = self.use_case.execute(input_param)
        entity = self.repo.find_by_id(output.id)
        
        self.assertEqual(entity.name, 'Movie3')
        self.assertEqual(entity.description, 'some description3')
        self.assertTrue(entity.is_active)
        
        input_param = CreateCategoryUseCase.Input(name='Movie4', description='some description4', is_active=False)
        
        output = self.use_case.execute(input_param)
        entity = self.repo.find_by_id(output.id)
        
        self.assertEqual(entity.name, 'Movie4')
        self.assertEqual(entity.description, 'some description4')
        self.assertFalse(entity.is_active)
        
        