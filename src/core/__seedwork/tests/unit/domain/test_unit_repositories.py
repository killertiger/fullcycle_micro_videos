import unittest
from dataclasses import InitVar, dataclass
from typing import Literal, Optional, List, Union
from core.__seedwork.domain.repositories import (
    ET,
    Filter,
    InMemoryRepository,
    InMemorySearchableRepository,
    RepositoryInterface,
    SearchParams,
    SearchableRepositoryInterface,
    SearchResult,
    SortDirection,
    SortDirectionValues,
)
from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityId


class TestRepositoryInterface(unittest.TestCase):
    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()  # pylint: disable=abstract-class-instantiated
        self.assertEqual(assert_error.exception.args[0],
                         "Can't instantiate abstract class RepositoryInterface with abstract " +
                         "methods bulk_insert, delete, find_all, find_by_id, insert, update"
                         )


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class TestInMemoryRepository(unittest.TestCase):
    repo: StubInMemoryRepository

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()

    def test_items_prop_is_empty_on_init(self):
        self.assertEqual(self.repo.items, [])

    def test_insert(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)
        self.assertEqual(self.repo.items, [entity])

    def test_throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'")

        unique_entity_id = UniqueEntityId(
            '2a181815-db58-43b1-81aa-597e69e66eb8')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID '2a181815-db58-43b1-81aa-597e69e66eb8'"
        )

    def test_find_by_id(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        entity_found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity_found, entity)

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(entity, entity_found)

    def test_find_all(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)
        entity2 = StubEntity(name='test2', price=10)
        self.repo.insert(entity2)

        items = self.repo.find_all()
        self.assertListEqual(items, [entity, entity2])

    def test_throw_not_found_exception_in_update(self):
        entity = StubEntity(name='test', price=5)

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(entity.id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

    def test_update(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        entity_updated = StubEntity(
            unique_entity_id=entity.unique_entity_id, name='updated', price=1)
        self.repo.update(entity_updated)

        self.assertEqual(entity_updated, self.repo.items[0])

    def test_throw_not_found_exception_in_delete(self):
        entity = StubEntity(name='test', price=5)

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

    def test_delete(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        self.repo.delete(entity.id)
        self.assertListEqual(self.repo.items, [])

        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        self.repo.delete(entity.unique_entity_id)
        self.assertListEqual(self.repo.items, [])


class TestSearchableRepositoryInterface(unittest.TestCase):

    def test_throw_error_when_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            SearchableRepositoryInterface()  # pylint: disable=abstract-class-instantiated
        self.assertEqual(assert_error.exception.args[0],
                         "Can't instantiate abstract class SearchableRepositoryInterface " +
                         "with abstract methods bulk_insert, delete, find_all, find_by_id, insert, " +
                         "search, update"
                         )

    def test_sortable_fields_prop(self):
        self.assertEqual(SearchableRepositoryInterface.sortable_fields, [])


class TestSearchParams(unittest.TestCase):
    maxDiff = None

#TODO: TEST TO BE FIXED    
    def test_props_annotations(self):
        self.assertEqual(SearchParams.__annotations__,
                         {
                             'page': Optional[int],
                             'per_page': Optional[int],
                             'sort': Optional[str],
                             'init_sort_dir': InitVar[SortDirectionValues | SortDirection | None],
                             'sort_dir': Optional[SortDirection],
                             'filter': Optional[Filter]
                         })

    def test_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.page, 1)

        arrange = [
            {'page': None, 'expected': 1},
            {'page': "", 'expected': 1},
            {'page': "fake", 'expected': 1},
            {'page': 0, 'expected': 1},
            {'page': -1, 'expected': 1},
            {'page': 5.5, 'expected': 5},
            {'page': "-1", 'expected': 1},
            {'page': True, 'expected': 1},
            {'page': False, 'expected': 1},
            {'page': {}, 'expected': 1},
            {'page': 1, 'expected': 1},
            {'page': 2, 'expected': 2},
        ]

        for i in arrange:
            params = SearchParams(page=i['page'])
            self.assertEqual(params.page, i['expected'])

    def test_per_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.per_page, 15)

        arrange = [
            {'per_page': None, 'expected': 15},
            {'per_page': "", 'expected': 15},
            {'per_page': "fake", 'expected': 15},
            {'per_page': 0, 'expected': 15},
            {'per_page': -1, 'expected': 15},
            {'per_page': 5.5, 'expected': 5},
            {'per_page': "-1", 'expected': 15},
            {'per_page': True, 'expected': 1},
            {'per_page': False, 'expected': 15},
            {'per_page': {}, 'expected': 15},
            {'per_page': 1, 'expected': 1},
            {'per_page': 2, 'expected': 2},
        ]

        for i in arrange:
            params = SearchParams(per_page=i['per_page'])
            self.assertEqual(params.per_page, i['expected'])

    def test_sort_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort)

        arrange = [
            {'sort': None, 'expected': None},
            {'sort': "", 'expected': None},
            {'sort': "fake", 'expected': 'fake'},
            {'sort': 0, 'expected': '0'},
            {'sort': -1, 'expected': '-1'},
            {'sort': "0", 'expected': '0'},
            {'sort': "-1", 'expected': '-1'},
            {'sort': 5.5, 'expected': '5.5'},
            {'sort': True, 'expected': 'True'},
            {'sort': False, 'expected': 'False'},
            {'sort': {}, 'expected': '{}'},
        ]

        for i in arrange:
            params = SearchParams(sort=i['sort'])
            self.assertEqual(params.sort, i['expected'])

    def test_sort_dir_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort=None)
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort='')
        self.assertIsNone(params.sort_dir)

        arrange = [
            {'sort_dir': None, 'expected': SortDirection.ASC},
            {'sort_dir': "", 'expected': SortDirection.ASC},
            {'sort_dir': "fake", 'expected': SortDirection.ASC},
            {'sort_dir': 0, 'expected': SortDirection.ASC},
            {'sort_dir': 'asc', 'expected': SortDirection.ASC},
            {'sort_dir': 'ASC', 'expected': SortDirection.ASC},
            {'sort_dir': 'desc', 'expected': SortDirection.DESC},
            {'sort_dir': 'DESC', 'expected': SortDirection.DESC},
        ]

        for i in arrange:
            params = SearchParams(sort='name', init_sort_dir=i['sort_dir'])
            self.assertEqual(
                params.sort_dir, i['expected'], f'sort_dir input: {i["sort_dir"]}')

    def test_filter_prop(self):
        params = SearchParams()
        self.assertIsNone(params.filter)

        arrange = [
            {'filter': None, 'expected': None},
            {'filter': "", 'expected': None},
            {'filter': "fake", 'expected': 'fake'},
            {'filter': 0, 'expected': '0'},
            {'filter': -1, 'expected': '-1'},
            {'filter': "0", 'expected': '0'},
            {'filter': "-1", 'expected': '-1'},
            {'filter': 5.5, 'expected': '5.5'},
            {'filter': True, 'expected': 'True'},
            {'filter': False, 'expected': 'False'},
            {'filter': {}, 'expected': '{}'},
        ]

        for i in arrange:
            params = SearchParams(filter=i['filter'])
            self.assertEqual(params.filter, i['expected'])


class TestSearchResult(unittest.TestCase):
    def test_props_annotations(self):
        self.assertEqual(SearchResult.__annotations__,
                         {
                             'items': List[ET],
                             'total': int,
                             'current_page': int,
                             'per_page': int,
                             'last_page': int,
                             'sort': Optional[str],
                             'sort_dir': Optional[str],
                             'filter': Optional[Filter]
                         })

    def test_constructor(self):
        entity = StubEntity(name='fake', price=5)
        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2
        )

        self.assertDictEqual(result.to_dict(),
                             {
                                 'items': [entity, entity],
                                 'total': 4,
                                 'current_page': 1,
                                 'per_page': 2,
                                 'last_page': 2,
                                 'sort': None,
                                 'sort_dir': None,
                                 'filter': None
        })

        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='test'
        )

        self.assertDictEqual(result.to_dict(),
                             {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': 'name',
            'sort_dir': 'asc',
            'filter': 'test'
        })

    def test_when_per_page_is_greater_than_total(self):
        result = SearchResult(
            items=[],
            total=4,
            current_page=1,
            per_page=15
        )
        self.assertEqual(result.last_page, 1)

    def test_when_per_page_is_less_than_total_and_they_are_not_multiples(self):
        result = SearchResult(
            items=[],
            total=101,
            current_page=1,
            per_page=20
        )
        self.assertEqual(result.last_page, 6)


class StubInMemorySearchableRepository(InMemorySearchableRepository[StubEntity, str]):
    sortable_fields: List[str] = ['name']

    def _apply_filter(self, items: List[StubEntity], filter_param: str | None) -> List[StubEntity]:
        if filter_param:
            filter_obj = filter(lambda i: filter_param.lower(
            ) in i.name.lower() or filter_param == str(i.price), items)
            return list(filter_obj)

        return items


class TestInMemorySearchableRepository(unittest.TestCase):
    repo: StubInMemorySearchableRepository

    def setUp(self) -> None:
        self.repo = StubInMemorySearchableRepository()

    def test__apply_filter(self):
        items = [StubEntity(name='test', price=5)]
        result = self.repo._apply_filter(  # pylint: disable=protected-access
            items, None)
        self.assertEqual(items, result)

        items = [
            StubEntity(name='test', price=5),
            StubEntity(name='TEST', price=5),
            StubEntity(name='fake', price=0),
        ]

        result = self.repo._apply_filter(  # pylint: disable=protected-access
            items, 'TEST')
        self.assertEqual([items[0], items[1]], result)

        result = self.repo._apply_filter(  # pylint: disable=protected-access
            items, '5')
        self.assertEqual([items[0], items[1]], result)

        result = self.repo._apply_filter(  # pylint: disable=protected-access
            items, '0')
        self.assertEqual([items[2]], result)

    def test__apply_sort(self):
        items = [
            StubEntity(name='b', price=5),
            StubEntity(name='a', price=2),
            StubEntity(name='c', price=0),
        ]

        result = self.repo._apply_sort(  # pylint: disable=protected-access
            items, 'price', SortDirection.ASC)
        self.assertEqual(items, result)

        result = self.repo._apply_sort(  # pylint: disable=protected-access
            items, 'name', SortDirection.ASC)
        self.assertEqual([items[1], items[0], items[2]], result)

        result = self.repo._apply_sort(  # pylint: disable=protected-access
            items, 'name', SortDirection.DESC)
        self.assertEqual([items[2], items[0], items[1]], result)

        self.repo.sortable_fields.append('price')
        result = self.repo._apply_sort(  # pylint: disable=protected-access
            items, 'price', SortDirection.ASC)
        self.assertEqual([items[2], items[1], items[0]], result)

        self.repo.sortable_fields.append('price')
        result = self.repo._apply_sort(  # pylint: disable=protected-access
            items, 'price', SortDirection.DESC)
        self.assertEqual([items[0], items[1], items[2]], result)

    def test__apply_paginate(self):
        items = [
            StubEntity(name='a', price=5),
            StubEntity(name='b', price=2),
            StubEntity(name='c', price=0),
            StubEntity(name='d', price=0),
            StubEntity(name='e', price=0),
        ]

        result = self.repo._apply_paginate(  # pylint: disable=protected-access
            items, 1, 2)
        self.assertEqual([items[0], items[1]], result)

        result = self.repo._apply_paginate(  # pylint: disable=protected-access
            items, 2, 2)
        self.assertEqual([items[2], items[3]], result)

        result = self.repo._apply_paginate(  # pylint: disable=protected-access
            items, 3, 2)
        self.assertEqual([items[4]], result)

        result = self.repo._apply_paginate(  # pylint: disable=protected-access
            items, 4, 2)
        self.assertEqual([], result)

    def test_search_when_params_is_empty(self):
        entity = StubEntity(name='a', price=1)
        items = [entity] * 16
        self.repo.items = items

        result = self.repo.search(SearchParams())
        self.assertEqual(result, SearchResult(
            items=[entity] * 15,
            total=16,
            current_page=1,
            per_page=15,
            sort=None,
            sort_dir=None,
            filter=None
        ))

    def test_search_applying_filter_and_paginate(self):
        items = [
            StubEntity(name='test', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='TEST', price=1),
            StubEntity(name='TeST', price=1),
        ]
        self.repo.items = items

        result = self.repo.search(SearchParams(
            page=1, per_page=2, filter='TEST'
        ))
        self.assertEqual(result, SearchResult(
            items=[items[0], items[2]],
            total=3,
            current_page=1,
            per_page=2,
            sort=None,
            sort_dir=None,
            filter='TEST'
        ))

        result = self.repo.search(SearchParams(
            page=2, per_page=2, filter='TEST'
        ))
        self.assertEqual(result, SearchResult(
            items=[items[3]],
            total=3,
            current_page=2,
            per_page=2,
            sort=None,
            sort_dir=None,
            filter='TEST'
        ))

        result = self.repo.search(SearchParams(
            page=3, per_page=2, filter='TEST'
        ))
        self.assertEqual(result, SearchResult(
            items=[],
            total=3,
            current_page=3,
            per_page=2,
            sort=None,
            sort_dir=None,
            filter='TEST'
        ))

    def test_search_applying_sort_and_paginate(self):
        items = [
            StubEntity(name='b', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='d', price=1),
            StubEntity(name='e', price=1),
            StubEntity(name='c', price=1),
        ]
        self.repo.items = items

        arrange_by_asc = [
            {
                'input': SearchParams(page=1, per_page=2, sort='name'),
                'output': SearchResult(
                    items=[items[1], items[0]],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir=SortDirection.ASC,
                    filter=None
                )
            },
            {
                'input': SearchParams(page=2, per_page=2, sort='name'),
                'output': SearchResult(
                    items=[items[4], items[2]],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort='name',
                    sort_dir=SortDirection.ASC,
                    filter=None
                )
            },
            {
                'input': SearchParams(page=3, per_page=2, sort='name'),
                'output': SearchResult(
                    items=[items[3]],
                    total=5,
                    current_page=3,
                    per_page=2,
                    sort='name',
                    sort_dir=SortDirection.ASC,
                    filter=None
                )
            },
        ]

        for index, item in enumerate(arrange_by_asc):
            result = self.repo.search(item['input'])
            self.assertEqual(result,
                             item['output'],
                             f'The output using sort_dir asc on index {index} is different')

        arrange_by_desc = [
            {
                'input': SearchParams(page=1, per_page=2, sort='name', init_sort_dir=SortDirection.DESC),
                'output': SearchResult(
                    items=[items[3], items[2]],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir=SortDirection.DESC,
                    filter=None
                )
            },
            {
                'input': SearchParams(page=2, per_page=2, sort='name', init_sort_dir=SortDirection.DESC),
                'output': SearchResult(
                    items=[items[4], items[0]],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort='name',
                    sort_dir=SortDirection.DESC,
                    filter=None
                )
            },
            {
                'input': SearchParams(page=3, per_page=2, sort='name', init_sort_dir=SortDirection.DESC),
                'output': SearchResult(
                    items=[items[1]],
                    total=5,
                    current_page=3,
                    per_page=2,
                    sort='name',
                    sort_dir=SortDirection.DESC,
                    filter=None
                )
            },
        ]

        for index, item in enumerate(arrange_by_desc):
            result = self.repo.search(item['input'])
            self.assertEqual(result,
                             item['output'],
                             f'The output using sort_dir desc on index {index} is different')

    def test_search_applying_filter_and_sort_and_paginate(self):
        items = [
            StubEntity(name='test', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='TEST', price=1),
            StubEntity(name='e', price=1),
            StubEntity(name='Test', price=1),
        ]
        self.repo.items = items

        result = self.repo.search(SearchParams(
            page=1, per_page=2, sort='name', init_sort_dir=SortDirection.ASC, filter='TEST'
        ))
        self.assertEqual(result, SearchResult(
            items=[items[2], items[4]],
            total=3,
            current_page=1,
            per_page=2,
            sort='name',
            sort_dir=SortDirection.ASC,
            filter='TEST'
        ))

        result = self.repo.search(SearchParams(
            page=2, per_page=2, sort='name', init_sort_dir=SortDirection.ASC, filter='TEST'
        ))
        self.assertEqual(result, SearchResult(
            items=[items[0]],
            total=3,
            current_page=2,
            per_page=2,
            sort='name',
            sort_dir=SortDirection.ASC,
            filter='TEST'
        ))
