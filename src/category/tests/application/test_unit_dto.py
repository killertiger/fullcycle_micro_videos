from typing import Optional
import unittest

from datetime import datetime
from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.domain.entities import Category

class TestCategoryOutputUnit(unittest.TestCase):
    def test_fields(self):
        self.assertEqual(CategoryOutput.__annotations__, {
            'id': str,
            'name': str,
            'description': Optional[str],
            'is_active': bool,
            'created_at': datetime
        })
        
class CategoryOuputChild(CategoryOutput):
    pass

        
class TestCategoryOutputMapperUnit(unittest.TestCase):
    
    def test_to_output_from_child(self):
        mapper = CategoryOutputMapper\
            .from_child(CategoryOuputChild)
        self.assertIsInstance(mapper, CategoryOutputMapper)
        self.assertTrue(
            issubclass(
                mapper.output_child,
                CategoryOuputChild
            )
        )

    def test_to_output_without_child(self):
        mapper = CategoryOutputMapper\
            .without_child()
        self.assertIsInstance(mapper, CategoryOutputMapper)
        self.assertTrue(
            issubclass(
                mapper.output_child,
                CategoryOutput
            )
        )
        
    def test_to_output(self):
        created_at = datetime.now()
        category = Category(
            name='test',
            description='some description',
            is_active=True,
            created_at=created_at
        )
        output = CategoryOutputMapper.without_child().to_output(category)
        self.assertEqual(output, CategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        ))
        
        output = CategoryOutputMapper.from_child(CategoryOuputChild).to_output(category)
        self.assertEqual(output, CategoryOuputChild(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        ))