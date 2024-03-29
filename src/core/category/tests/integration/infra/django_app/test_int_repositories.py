import datetime
import unittest
from django.utils import timezone
from model_bakery.utils import seq
import pytest
from model_bakery import baker
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.infra.category_django_app.mapper import CategoryModelMapper
from core.category.infra.category_django_app.repositories import CategoryDjangoRepository
from core.category.infra.category_django_app.models import CategoryModel
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

    def test_search_applying_filter_and_paginate(self):
        default_props = {
            'description': None,
            'is_active': True,
            'created_at': timezone.now(),
        }

        models = CategoryModel.objects.bulk_create(
            [
                CategoryModel(id=UniqueEntityId().id, name='test', **default_props),
                CategoryModel(id=UniqueEntityId().id, name='a', **default_props),
                CategoryModel(id=UniqueEntityId().id, name='TEST', **default_props),
                CategoryModel(id=UniqueEntityId().id, name='TeSt', **default_props),
            ]
        )

        search_params = CategoryRepository.SearchParams(page=1, per_page=2, filter='E')

        search_result = self.repo.search(search_params)

        self.assertEqual(
            search_result,
            CategoryRepository.SearchResult(
                items=[
                    CategoryModelMapper.to_entity(models[0]),
                    CategoryModelMapper.to_entity(models[2]),
                ],
                total=3,
                current_page=1,
                per_page=2,
                sort=None,
                sort_dir=None,
                filter='E',
            ),
        )

    def test_search_applying_paginate_and_sort(self):
        default_props = {
            'description': None,
            'is_active': True,
            'created_at': timezone.now(),
        }

        category_model_name_list = ['b', 'a', 'd', 'e', 'c']

        category_model_list = [
            CategoryModel(id=UniqueEntityId().id, name=name, **default_props)
            for name in category_model_name_list
        ]

        models = CategoryModel.objects.bulk_create(category_model_list)

        arrange_by_asc = [
            {
                'search_params': CategoryDjangoRepository.SearchParams(
                    per_page=2, sort='name'
                ),
                'search_output': CategoryDjangoRepository.SearchResult(
                    items=[
                        CategoryModelMapper.to_entity(models[1]),
                        CategoryModelMapper.to_entity(models[0]),
                    ],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir='asc',
                    filter=None,
                ),
            },
            {
                'search_params': CategoryDjangoRepository.SearchParams(
                    page=2, per_page=2, sort='name'
                ),
                'search_output': CategoryDjangoRepository.SearchResult(
                    items=[
                        CategoryModelMapper.to_entity(models[4]),
                        CategoryModelMapper.to_entity(models[2]),
                    ],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort='name',
                    sort_dir='asc',
                    filter=None,
                ),
            },
        ]

        for index, item in enumerate(arrange_by_asc):
            search_output = self.repo.search(item['search_params'])
            self.assertEqual(
                search_output,
                item['search_output'],
                f"The output using sort_dir asc on index {index} is different",
            )

        arrange_by_desc = [
            {
                'search_params': CategoryDjangoRepository.SearchParams(
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                ),
                'search_output': CategoryDjangoRepository.SearchResult(
                    items=[
                        CategoryModelMapper.to_entity(models[3]),
                        CategoryModelMapper.to_entity(models[2]),
                    ],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None,
                ),
            },
            {
                'search_params': CategoryDjangoRepository.SearchParams(
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                ),
                'search_output': CategoryDjangoRepository.SearchResult(
                    items=[
                        CategoryModelMapper.to_entity(models[3]),
                        CategoryModelMapper.to_entity(models[2]),
                    ],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None,
                ),
            },
            {
                'search_params': CategoryDjangoRepository.SearchParams(
                    page=2,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                ),
                'search_output': CategoryDjangoRepository.SearchResult(
                    items=[
                        CategoryModelMapper.to_entity(models[4]),
                        CategoryModelMapper.to_entity(models[0]),
                    ],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None,
                ),
            },
        ]

        for index, item in enumerate(arrange_by_desc):
            search_output = self.repo.search(item['search_params'])
            self.assertEqual(
                search_output,
                item['search_output'],
                f"The output using sort_dir desc on index {index} is different",
            )

    def test_search_applying_filter_sort_and_paginate(self):
        default_props = {
            'description': None,
            'is_active': True,
            'created_at': timezone.now(),
        }

        category_model_name_list = ['test', 'a', 'TEST', 'e', 'TeSt']

        category_model_list = [
            CategoryModel(id=UniqueEntityId().id, name=name, **default_props)
            for name in category_model_name_list
        ]
        
        models = CategoryModel.objects.bulk_create(category_model_list)
        
        search_result = self.repo.search(CategoryRepository.SearchParams(
            page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='TEST'
        ))
        self.assertEqual(search_result, CategoryDjangoRepository.SearchResult(
            items=[
                CategoryModelMapper.to_entity(models[2]),
                CategoryModelMapper.to_entity(models[4]),
            ],
            total=3,
            current_page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='TEST',
        ))
        
        search_result = self.repo.search(CategoryRepository.SearchParams(
            page=2,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='TEST'
        ))
        self.assertEqual(search_result, CategoryDjangoRepository.SearchResult(
            items=[
                CategoryModelMapper.to_entity(models[0]),
            ],
            total=3,
            current_page=2,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='TEST',
        ))
