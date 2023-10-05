from typing import OrderedDict
import unittest
from rest_framework import serializers
from core.__seedwork.infra.django_app.serializers import (
    CollectionSerializer,
    PaginationSerializer,
    PaginationOutput,
    ResourceSerializer,
)


class TestPaginationSerializer(unittest.TestCase):
    def test_serialize(self):
        pagination = {
            'current_page': '1',
            'per_page': '2',
            'last_page': '3',
            'total': '4',
        }
        data = PaginationSerializer(pagination).data

        self.assertEqual(
            data, {'current_page': 1, 'per_page': 2, 'last_page': 3, 'total': 4}
        )


class StubSerializer(ResourceSerializer):
    name = serializers.CharField()


class StubCollectionSerializer(CollectionSerializer):
    child = StubSerializer()


class TestCollectionSerializer(unittest.TestCase):
    def test_if_throw_an_error_if_is_not_a_pagination_instance(self):
        error_message = 'instance must be a PaginationOutput'

        with self.assertRaises(TypeError) as assert_exception:
            CollectionSerializer()
        self.assertEqual(str(assert_exception.exception), error_message)

        with self.assertRaises(TypeError) as assert_exception:
            CollectionSerializer(instance={})
        self.assertEqual(str(assert_exception.exception), error_message)

        with self.assertRaises(TypeError) as assert_exception:
            CollectionSerializer(instance=1)
        self.assertEqual(str(assert_exception.exception), error_message)

    def test__init__(self):
        pagination = PaginationOutput(
            items=[1, 2, 3], total=3, current_page=1, per_page=3, last_page=1
        )

        collection = StubCollectionSerializer(instance=pagination)
        self.assertEqual(collection.pagination, pagination)
        self.assertEqual(collection.instance, pagination.items)

    def test_serialize(self):
        pagination = PaginationOutput(
            items=[{'name': 'foo'}, {'name': 'bar'}],
            total=3,
            current_page=1,
            per_page=3,
            last_page=1,
        )

        data = StubCollectionSerializer(instance=pagination).data
        self.assertEqual(
            data,
            {
                'data': [
                    OrderedDict([('name', 'foo')]),
                    OrderedDict([('name', 'bar')]),
                ],
                'meta': {'total': 3, 'current_page': 1, 'per_page': 3, 'last_page': 1},
            },
        )
