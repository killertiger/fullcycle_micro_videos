from datetime import datetime
from dataclasses import FrozenInstanceError, is_dataclass
from unittest.mock import patch
import unittest

from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        with patch.object(Category, 'validate') as mock_validate_method:
            category = Category(name='Movie')
            mock_validate_method.assert_called_once()
            self.assertEqual(category.name, 'Movie')
            self.assertEqual(category.description, None)
            self.assertEqual(category.is_active, True)
            self.assertIsInstance(category.created_at, datetime)

            created_at = datetime.now()
            category = Category(
                name='Movie',
                description='some description',
                is_active=False,
                created_at=created_at
            )
            self.assertEqual(category.name, 'Movie')
            self.assertEqual(category.description, 'some description')
            self.assertEqual(category.is_active, False)
            self.assertEqual(category.created_at, created_at)

    def test_if_created_at_is_generated_in_constructor(self):
        with patch.object(Category, 'validate'):
            category1 = Category(name='Movie 1')
            category2 = Category(name='Movie 2')

            self.assertNotEqual(category1.created_at, category2.created_at)

    def test_if_is_immutable(self):
        with patch.object(Category, 'validate'):
            with self.assertRaises(FrozenInstanceError):
                object_value = Category(name='Movie 1')
                object_value.name = 'fake name'

    def test_activate(self):
        with patch.object(Category, 'validate'):
            category = Category(name='Movie 1', is_active=False)

            category.activate()

            self.assertTrue(category.is_active)

    def test_deactivate(self):
        with patch.object(Category, 'validate'):
            category = Category(name='Movie 1', is_active=True)

            category.deactivate()

            self.assertFalse(category.is_active)

    def test_update(self):
        with patch.object(Category, 'validate'):
            category = Category(name='Movie 1', description='My description')

            category.update(name='Name 2', description='My new description')

            self.assertEqual(category.name, 'Name 2')
            self.assertEqual(category.description, 'My new description')
