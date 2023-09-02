import unittest
from core.category.domain.entities import Category
from django.utils import timezone
from core.category.infra.django_app.mapper import CategoryModelMapper
from core.category.infra.django_app.models import CategoryModel


class TestCategoryModelMapper(unittest.TestCase):
    
    def test_to_entity(self):
        created_at = timezone.now()
        
        model = CategoryModel(
            id='2a181815-db58-43b1-81aa-597e69e66eb8',
            name='Movie',
            description='Movie description',
            is_active=True,
            created_at=created_at,
        )
        
        entity = CategoryModelMapper.to_entity(model)
        
        self.assertEqual(str(entity.id), '2a181815-db58-43b1-81aa-597e69e66eb8')
        self.assertEqual(entity.name, 'Movie')
        self.assertEqual(entity.description, 'Movie description')
        self.assertTrue(entity.is_active)
        self.assertEqual(entity.created_at, created_at)
        
    
    def test_to_model(self):
        entity = Category(
            name='Movie',
            description='Movie description',
            is_active=True,
        )
        
        model = CategoryModelMapper.to_model(entity)
        
        self.assertEqual(str(model.id), entity.id)
        self.assertEqual(model.name, 'Movie')
        self.assertEqual(model.description, 'Movie description')
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, entity.created_at)