import unittest
from datetime import datetime
from category.domain.entities import Category

from category.domain.repositories import CategoryInMemoryRepository, CategoryRepository

class TestCategoryInMemoryRepository(unittest.TestCase):
    repo: CategoryInMemoryRepository
    
    def setUp(self) -> None:
        self.repo = CategoryInMemoryRepository()
        
    
    def test_filter_and_sort(self):
        self.repo.insert(Category('8fffa1fd-8cc5-40a5-b9e9-961ba7ee93dc', name='Action', created_at=datetime(2023, 1, 15)))
        self.repo.insert(Category('076ced7e-6b3d-4f9f-9cee-d7ddade5b02a', name='Comedy', created_at=datetime(2023, 1, 13)))
        self.repo.insert(Category('50fed266-1a0e-11ee-be56-0242ac120002', name='Drama', created_at=datetime(2023, 11, 5)))
        self.repo.insert(Category('5497cafe-1a0e-11ee-be56-0242ac120002', name='Fantasy', created_at=datetime(2023, 4, 13)))
        self.repo.insert(Category('8d16fd4b-3caf-4bc6-9c9b-76f7bc1e639b', name='Horror', created_at=datetime(2023, 5, 25)))
        self.repo.insert(Category('8d16fd4b-3caf-4bc6-9c9b-76f7bc1e639b', name='Mystery', created_at=datetime(2023, 12, 6)))
        self.repo.insert(Category('8d16fd4b-3caf-4bc6-9c9b-76f7bc1e639b', name='Romance', created_at=datetime(2023, 7, 18)))
        self.repo.insert(Category('8d16fd4b-3caf-4bc6-9c9b-76f7bc1e639b', name='Thriller', created_at=datetime(2023, 9, 17)))
        
        result = self.repo.search(CategoryRepository.SearchParams(filter='comedy'))
        
        self.assertEqual(result.items, [
            Category('076ced7e-6b3d-4f9f-9cee-d7ddade5b02a', name='Comedy', created_at=datetime(2023, 1, 13))
        ])
        
        result = self.repo.search(CategoryRepository.SearchParams(filter='ma'))
        
        self.assertEqual(result.items, [
            Category('8d16fd4b-3caf-4bc6-9c9b-76f7bc1e639b', name='Romance', created_at=datetime(2023, 7, 18)),
            Category('50fed266-1a0e-11ee-be56-0242ac120002', name='Drama', created_at=datetime(2023, 11, 5)),
        ])
        
        result = self.repo.search(CategoryRepository.SearchParams(filter='ma', sort='name'))
        
        self.assertEqual(result.items, [
            Category('50fed266-1a0e-11ee-be56-0242ac120002', name='Drama', created_at=datetime(2023, 11, 5)),
            Category('8d16fd4b-3caf-4bc6-9c9b-76f7bc1e639b', name='Romance', created_at=datetime(2023, 7, 18)),
        ])