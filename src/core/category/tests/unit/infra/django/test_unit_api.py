from collections import namedtuple
from datetime import datetime
import unittest
from unittest import mock
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from core.__seedwork.infra.serializers import UUIDSerializer
from core.category.application.dto import CategoryOutput
from core.category.infra.django_app.serializer import CategorySerializer
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase,
)
from core.category.infra.django_app.api import CategoryResource
from core.category.tests.helpers import init_category_resource_all_none


class StubCategorySerializer:
    validated_data = None

    def is_valid(self, raise_exception: bool):
        pass


class TestCategoryResourceUnit(unittest.TestCase):
    @mock.patch.object(CategorySerializer, '__new__')
    def test_category_to_response_method(self, mock_serializer):
        mock_serializer.return_value = namedtuple('Faker', ['data'])(
            data='test'
        )  # creates a typed class on the fly
        data = CategoryResource.category_to_response('output')
        mock_serializer.assert_called_with(CategorySerializer, instance='output')
        self.assertEqual(data, 'test')
        
    @mock.patch.object(UUIDSerializer, '__new__')    
    def test_validate_id_method(self, mock_serializer):
        mock_serializer_is_valid = mock.MagicMock()
        mock_serializer.return_value = namedtuple(
            'Fake', ['is_valid'])\
                (is_valid=mock_serializer_is_valid)
        CategoryResource.validate_id('fake id')
        mock_serializer.assert_called_with(
            UUIDSerializer,
            data={'id': 'fake id'}
        )
        mock_serializer_is_valid.assert_called_with(
            raise_exception=True
        )

    @mock.patch.object(CategoryResource, 'category_to_response')
    def test_post_method(self, mock_category_to_response):
        stub_serializer = StubCategorySerializer()
        send_data = {"name": "fake name"}

        expected_response = {
            'id': 'fc98cf57-4615-4b0a-b5eb-373870ca27ce',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': datetime.now(),
        }

        with mock.patch.object(
            CategorySerializer, '__new__', return_value=stub_serializer
        ) as mock_serializer:
            stub_serializer.validated_data = send_data
            stub_serializer.is_valid = mock.MagicMock()

            mock_create_use_case = mock.Mock(CreateCategoryUseCase)

            mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
                **expected_response
            )

            mock_category_to_response.return_value = expected_response

            resource = CategoryResource(
                **{
                    **init_category_resource_all_none(),
                    "create_use_case": lambda: mock_create_use_case,
                }
            )

            _request = APIRequestFactory().post("", send_data)
            request = Request(_request)
            request._full_data = send_data

            response = resource.post(request)

            stub_serializer.is_valid.assert_called_with(raise_exception=True)
            mock_create_use_case.execute.assert_called_with(
                CreateCategoryUseCase.Input(name="fake name")
            )
            mock_category_to_response.assert_called_with(
                mock_create_use_case.execute.return_value
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                response.data,
                {
                    "id": "fc98cf57-4615-4b0a-b5eb-373870ca27ce",
                    "name": "Movie",
                    "description": None,
                    "is_active": True,
                    "created_at": expected_response['created_at'],
                },
            )
        mock_serializer.assert_called_with(CategorySerializer, data=send_data)

    def test_list_method(self):
        mock_list_use_case = mock.Mock(ListCategoriesUseCase)
        mock_list_use_case.execute.return_value = ListCategoriesUseCase.Output(
            items=[
                CategoryOutput(
                    id="fc98cf57-4615-4b0a-b5eb-373870ca27ce",
                    name="Movie",
                    description=None,
                    is_active=True,
                    created_at=datetime.now(),
                )
            ],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1,
        )

        resource = CategoryResource(
            **{
                **init_category_resource_all_none(),
                "list_use_case": lambda: mock_list_use_case,
            }
        )

        _request = APIRequestFactory().get(
            "/?page=1&per_page=1&sort=name&sort_dir=asc&filter=test"
        )
        request = Request(_request)

        response = resource.get(request)

        mock_list_use_case.execute.assert_called_with(
            ListCategoriesUseCase.Input(
                page="1", per_page="1", sort="name", sort_dir="asc", filter="test"
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "items": [
                    {
                        "id": "fc98cf57-4615-4b0a-b5eb-373870ca27ce",
                        "name": "Movie",
                        "description": None,
                        "is_active": True,
                        "created_at": mock_list_use_case.execute.return_value.items[
                            0
                        ].created_at,
                    },
                ],
                "total": 1,
                "current_page": 1,
                "per_page": 2,
                "last_page": 1,
            },
        )

    @mock.patch.object(CategoryResource, 'category_to_response')
    @mock.patch.object(CategoryResource, 'validate_id')
    def test_if_get_invoke_get_object(self, mock_validate_id, mock_category_to_response):
        mock_get_use_case = mock.Mock(GetCategoryUseCase)
        mock_list_use_case = mock.Mock(ListCategoriesUseCase)
        uuid_value = 'fc98cf57-4615-4b0a-b5eb-373870ca27ce'
        
        expected_response = {
            'id': uuid_value,
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': datetime.now()
        }

        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            **expected_response
        )
        mock_category_to_response.return_value = {
            **expected_response,
        }

        resource = CategoryResource(
            **{
                **init_category_resource_all_none(),
                "get_use_case": lambda: mock_get_use_case,
                "list_use_case": lambda: mock_list_use_case,
            }
        )

        response = resource.get(None, uuid_value)

        self.assertEqual(mock_list_use_case.call_count, 0)
        mock_validate_id.assert_called_with(uuid_value)
        mock_get_use_case.execute.assert_called_with(
            GetCategoryUseCase.Input(id=uuid_value)
        )
        mock_category_to_response.assert_called_with(mock_get_use_case.execute.return_value)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            expected_response,
        )

    def test_if_get_invoke_get_object_2(self):
        resource = CategoryResource(**init_category_resource_all_none())
        resource.get_object = mock.Mock()
        resource.get(None, "fc98cf57-4615-4b0a-b5eb-373870ca27ce")
        resource.get_object.assert_called_once()

    def test_get_method(self):
        mock_get_use_case = mock.Mock(GetCategoryUseCase)

        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id="fc98cf57-4615-4b0a-b5eb-373870ca27ce",
            name="Movie",
            description=None,
            is_active=True,
            created_at=datetime.now(),
        )

        resource = CategoryResource(
            **{
                **init_category_resource_all_none(),
                "get_use_case": lambda: mock_get_use_case,
            }
        )

        response = resource.get_object("fc98cf57-4615-4b0a-b5eb-373870ca27ce")

        mock_get_use_case.execute.assert_called_with(
            GetCategoryUseCase.Input(id="fc98cf57-4615-4b0a-b5eb-373870ca27ce")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "id": "fc98cf57-4615-4b0a-b5eb-373870ca27ce",
                "name": "Movie",
                "description": None,
                "is_active": True,
                "created_at": mock_get_use_case.execute.return_value.created_at,
            },
        )

    def test_update_method(self):
        send_data = {"id": "fc98cf57-4615-4b0a-b5eb-373870ca27ce", "name": "Movie"}

        mock_update_use_case = mock.Mock(UpdateCategoryUseCase)

        mock_update_use_case.execute.return_value = UpdateCategoryUseCase.Output(
            id=send_data["id"],
            name=send_data["name"],
            description=None,
            is_active=True,
            created_at=datetime.now(),
        )

        resource = CategoryResource(
            **{
                **init_category_resource_all_none(),
                "update_use_case": lambda: mock_update_use_case,
            }
        )

        _request = APIRequestFactory().put("/", send_data)
        request = Request(_request)
        request._full_data = send_data

        response = resource.put(request, send_data["id"])

        mock_update_use_case.execute.assert_called_with(
            UpdateCategoryUseCase.Input(
                id=send_data["id"],
                name=send_data["name"],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "id": send_data["id"],
                "name": send_data["name"],
                "description": None,
                "is_active": True,
                "created_at": mock_update_use_case.execute.return_value.created_at,
            },
        )

    def test_delete_method(self):
        mock_delete_use_case = mock.Mock(DeleteCategoryUseCase)

        resource = CategoryResource(
            **{
                **init_category_resource_all_none(),
                "delete_use_case": lambda: mock_delete_use_case,
            }
        )

        _request = APIRequestFactory().delete("/")
        request = Request(_request)

        response = resource.delete(request, "fc98cf57-4615-4b0a-b5eb-373870ca27ce")

        mock_delete_use_case.execute.assert_called_with(
            DeleteCategoryUseCase.Input(id="fc98cf57-4615-4b0a-b5eb-373870ca27ce")
        )

        self.assertEqual(response.status_code, 204)
