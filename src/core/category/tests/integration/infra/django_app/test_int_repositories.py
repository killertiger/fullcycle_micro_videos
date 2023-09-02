import datetime
import unittest
from django.utils import timezone
from model_bakery.utils import seq
import pytest
from model_bakery import baker
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.infra.django_app.mapper import CategoryModelMapper
from core.category.infra.django_app.repositories import CategoryDjangoRepository
from core.category.infra.django_app.models import CategoryModel
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository


@pytest.mark.django_db
class TestCategoryDjangoRepositoryInt(unittest.TestCase):
    repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()

    def test_insert(self):
        category = Category(
            name='Movie',
        )

        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, 'Movie')
        self.assertIsNone(model.description)
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

        category = Category(
            name='Movie 2',
            description='Movie Description',
            is_active=False,
        )

        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, 'Movie 2')
        self.assertEqual(model.description, 'Movie Description')
        self.assertFalse(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

    def test_throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'"
        )

        unique_entity_id = UniqueEntityId('2a181815-db58-43b1-81aa-597e69e66eb8')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID '2a181815-db58-43b1-81aa-597e69e66eb8'",
        )

    def test_find_by_id(self):
        category = Category(
            name='Movie',
        )
        self.repo.insert(category)

        category_found = self.repo.find_by_id(category.id)
        self.assertEqual(category_found, category)

        category_found = self.repo.find_by_id(category.unique_entity_id)
        self.assertEqual(category_found, category)

    def test_find_all(self):
        models = baker.make(CategoryModel, _quantity=2)
        categories = self.repo.find_all()

        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0], CategoryModelMapper.to_entity(models[0]))
        self.assertEqual(categories[1], CategoryModelMapper.to_entity(models[1]))

    def test_throw_not_found_exception_in_update(self):
        entity = Category(name='Movie')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'"
        )

    def test_update(self):
        category = Category(name='Movie')
        self.repo.insert(category)

        category.update(name='Movie updated', description='description updated')
        self.repo.update(category)

        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, 'Movie updated')
        self.assertEqual(model.description, 'description updated')
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

    def test_throw_not_found_exception_in_delete(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete('fake id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'"
        )

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete('2a181815-db58-43b1-81aa-597e69e66eb8')
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID '2a181815-db58-43b1-81aa-597e69e66eb8'",
        )

        unique_entity_id = UniqueEntityId('2a181815-db58-43b1-81aa-597e69e66eb8')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID '2a181815-db58-43b1-81aa-597e69e66eb8'",
        )

    def test_delete(self):
        category = Category(name='Movie')
        self.repo.insert(category)

        self.repo.delete(category.id)

        with self.assertRaises(NotFoundException):
            self.repo.find_by_id(category.id)

        category = Category(name='Movie')
        self.repo.insert(category)

        self.repo.delete(category.unique_entity_id)

        with self.assertRaises(NotFoundException):
            self.repo.find_by_id(category.id)

    def test_search_when_params_is_empty(self):
        models = baker.make(
            CategoryModel,
            _quantity=16,
            created_at=seq(datetime.datetime.now(), datetime.timedelta(days=1)),
        )
        models.reverse()

        search_result = self.repo.search(CategoryRepository.SearchParams())
        self.assertIsInstance(search_result, CategoryRepository.SearchResult)
        self.assertEqual(
            search_result,
            CategoryRepository.SearchResult(
                items=[CategoryModelMapper.to_entity(model) for model in models[:15]],
                total=16,
                current_page=1,
                per_page=15,
                sort=None,
                sort_dir=None,
                filter=None,
            ),
        )
