import datetime
import unittest
import pytest
from core.__seedwork.domain.exceptions import NotFoundException
from core.category.domain.entities import Category
from core.category.application.dto import CategoryOutput, CategoryOutputMapper
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase,
)
from core.category.infra.category_django_app.repositories import CategoryDjangoRepository


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

        self.assertEqual(
            output,
            CreateCategoryUseCase.Output(
                id=entity.id,
                name='Movie',
                description=None,
                is_active=True,
                created_at=entity.created_at,
            ),
        )

        self.assertEqual(entity.name, 'Movie')
        self.assertIsNone(entity.description)
        self.assertTrue(entity.is_active)

        input_param = CreateCategoryUseCase.Input(
            name='Movie2', description='some description'
        )

        output = self.use_case.execute(input_param)
        entity = self.repo.find_by_id(output.id)

        self.assertEqual(
            output,
            CreateCategoryUseCase.Output(
                id=entity.id,
                name='Movie2',
                description='some description',
                is_active=True,
                created_at=entity.created_at,
            ),
        )
        self.assertEqual(entity.name, 'Movie2')
        self.assertEqual(entity.description, 'some description')
        self.assertTrue(entity.is_active)

        input_param = CreateCategoryUseCase.Input(
            name='Movie3', description='some description3'
        )

        output = self.use_case.execute(input_param)
        entity = self.repo.find_by_id(output.id)

        self.assertEqual(entity.name, 'Movie3')
        self.assertEqual(entity.description, 'some description3')
        self.assertTrue(entity.is_active)

        input_param = CreateCategoryUseCase.Input(
            name='Movie4', description='some description4', is_active=False
        )

        output = self.use_case.execute(input_param)
        entity = self.repo.find_by_id(output.id)

        self.assertEqual(entity.name, 'Movie4')
        self.assertEqual(entity.description, 'some description4')
        self.assertFalse(entity.is_active)


@pytest.mark.django_db
class TestGetCategoryUseCaseInt(unittest.TestCase):
    use_case: GetCategoryUseCase
    repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()
        self.use_case = GetCategoryUseCase(self.repo)

    def test_throws_exception_when_category_not_found(self):
        input_param = GetCategoryUseCase.Input('fake id')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'"
        )

    def test_execute(self):
        entity = Category.fake().a_category().build()
        self.repo.insert(entity)

        input_param = GetCategoryUseCase.Input(entity.id)
        output = self.use_case.execute(input_param)

        self.assertEqual(
            output,
            GetCategoryUseCase.Output(
                id=str(entity.id),
                name=entity.name,
                description=entity.description,
                is_active=entity.is_active,
                created_at=entity.created_at,
            ),
        )


@pytest.mark.django_db
class TestListCategoriesUseCaseInt(unittest.TestCase):
    use_case: ListCategoriesUseCase
    repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()
        self.use_case = ListCategoriesUseCase(self.repo)

    def from_entity_to_output(self, entity: Category) -> CategoryOutput:
        return CategoryOutputMapper.without_child().to_output(entity)

    def test_execute_using_empty_search_params(self):
        categories = Category.fake().the_categories(2)\
            .with_created_at(
                lambda index: datetime.datetime.now(
                    datetime.timezone.utc) + datetime.timedelta(days=index)
        ).build()

        self.repo.bulk_insert(categories)

        input_param = ListCategoriesUseCase.Input()
        output = self.use_case.execute(input_param)

        self.assertEqual(
            output,
            ListCategoriesUseCase.Output(
                items=[
                    self.from_entity_to_output(categories[1]),
                    self.from_entity_to_output(categories[0]),
                ],
                total=2,
                current_page=1,
                per_page=15,
                last_page=1,
            ),
        )

    def test_execute_using_pagination_and_sort_and_filter(self):
        faker = Category.fake().a_category()

        entities = [
            faker.with_name('a').build(),
            faker.with_name('AAA').build(),
            faker.with_name('AaA').build(),
            faker.with_name('b').build(),
            faker.with_name('C').build(),
        ]
        
        self.repo.bulk_insert(entities)

        input_param = ListCategoriesUseCase.Input(
            page=1, per_page=2, sort='name', sort_dir='asc', filter='a'
        )

        output = self.use_case.execute(input_param)

        self.assertEqual(
            output,
            ListCategoriesUseCase.Output(
                items=[
                    self.from_entity_to_output(entities[1]),
                    self.from_entity_to_output(entities[2]),
                ],
                total=3,
                current_page=1,
                per_page=2,
                last_page=2,
            ),
        )

        input_param = ListCategoriesUseCase.Input(
            page=2, per_page=2, sort='name', sort_dir='asc', filter='a'
        )

        output = self.use_case.execute(input_param)

        self.assertEqual(
            output,
            ListCategoriesUseCase.Output(
                items=[
                    self.from_entity_to_output(entities[0]),
                ],
                total=3,
                current_page=2,
                per_page=2,
                last_page=2,
            ),
        )

        input_param = ListCategoriesUseCase.Input(
            page=1, per_page=2, sort='name', sort_dir='desc', filter='a'
        )

        output = self.use_case.execute(input_param)

        self.assertEqual(
            output,
            ListCategoriesUseCase.Output(
                items=[
                    self.from_entity_to_output(entities[0]),
                    self.from_entity_to_output(entities[2]),
                ],
                total=3,
                current_page=1,
                per_page=2,
                last_page=2,
            ),
        )


@pytest.mark.django_db
class TestUpdateCategoryUseCaseInt(unittest.TestCase):
    use_case: UpdateCategoryUseCase
    repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()
        self.use_case = UpdateCategoryUseCase(self.repo)

    def test_throw_exception_when_category_not_found(self):
        request = UpdateCategoryUseCase.Input(id='not_found', name='test')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(request)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'not_found'"
        )

    def test_execute(self):
        entity = Category.fake().a_category().build()
        self.repo.insert(entity)
        
        request = UpdateCategoryUseCase.Input(id=entity.id, name='test 1')
        response = self.use_case.execute(request)
        self.assertEqual(
            response,
            UpdateCategoryUseCase.Output(
                id=str(entity.id),
                name='test 1',
                description=None,
                is_active=True,
                created_at=entity.created_at,
            ),
        )

        arrange = [
            {
                'input': {
                    'id': str(entity.id),
                    'name': 'test 2',
                    'description': 'description 2',
                },
                'expected': {
                    'id': str(entity.id),
                    'name': 'test 2',
                    'description': 'description 2',
                    'is_active': True,
                    'created_at': entity.created_at,
                },
            },
            {
                'input': {
                    'id': str(entity.id),
                    'name': 'test 3',
                    'description': 'description 3',
                    'is_active': False,
                },
                'expected': {
                    'id': str(entity.id),
                    'name': 'test 3',
                    'description': 'description 3',
                    'is_active': False,
                    'created_at': entity.created_at,
                },
            },
            {
                'input': {'id': str(entity.id), 'name': 'test 4', 'is_active': True},
                'expected': {
                    'id': str(entity.id),
                    'name': 'test 4',
                    'description': None,
                    'is_active': True,
                    'created_at': entity.created_at,
                },
            },
        ]

        for item in arrange:
            input_param = item['input']
            expected = item['expected']
            request = UpdateCategoryUseCase.Input(**input_param)
            category_output = self.use_case.execute(request)
            self.assertEqual(
                category_output, UpdateCategoryUseCase.Output(**expected))
            category = self.repo.find_by_id(expected['id'])
            self.assertEqual(category.name, expected['name'])
            self.assertEqual(category.description, expected['description'])
            self.assertEqual(category.is_active, expected['is_active'])
            self.assertEqual(category.created_at, expected['created_at'])


@pytest.mark.django_db
class TestDeleteCategoryUseCaseInt(unittest.TestCase):

    repo: CategoryDjangoRepository
    use_case: DeleteCategoryUseCase

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()
        self.use_case = DeleteCategoryUseCase(self.repo)

    def test_throw_exception_when_category_not_found(self):
        request = DeleteCategoryUseCase.Input(id='not_found')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(request)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'not_found'"
        )

    def test_execute(self):
        entity = Category.fake().a_category().build()
        self.repo.insert(entity)
        
        request = DeleteCategoryUseCase.Input(id=str(entity.id))
        self.use_case.execute(request)

        with self.assertRaises(NotFoundException):
            self.repo.find_by_id(str(entity.id))
