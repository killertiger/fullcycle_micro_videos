from datetime import datetime
import unittest
from django.utils import timezone
import pytest
from core.category.infra.django_app.models import CategoryModel


@pytest.mark.django_db()
class TestCategoryModelInt(unittest.TestCase):
    def test_create(self):
        arrange = {
            'id': 'f325c276-4d9e-47a2-a4ce-c151bd0e0074',
            'name': 'Movie',
            # 'description': None,
            'is_active': True,
            'created_at': timezone.now(),
        }

        category = CategoryModel.objects.create(**arrange)
        self.assertEqual(category.id, arrange['id'])
        self.assertEqual(category.name, arrange['name'])
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, arrange['is_active'])
        self.assertEqual(category.created_at, arrange['created_at'])
