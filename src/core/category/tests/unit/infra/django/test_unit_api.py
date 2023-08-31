from datetime import datetime
import unittest
from unittest import mock
from core.category.application.dto import CategoryOutput
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
)
from core.category.infra.django.api import CategoryResource


class TestCategoryResourceUnit(unittest.TestCase):
    def __init_all_none(self):
        return {"list_use_case": None, "create_use_case": None}

    def test_post_method(self):
        send_data = {"name": "fake name"}
        mock_create_use_case = mock.Mock(CreateCategoryUseCase)

        mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
            id="fc98cf57-4615-4b0a-b5eb-373870ca27ce",
            name="Movie",
            description=None,
            is_active=True,
            created_at=datetime.now(),
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                "create_use_case": lambda: mock_create_use_case,
            }
        )

        _request = APIRequestFactory().post("", send_data)
        request = Request(_request)
        request._full_data = send_data

        response = resource.post(request)

        mock_create_use_case.execute.assert_called_with(
            CreateCategoryUseCase.Input(name="fake name")
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                "id": "fc98cf57-4615-4b0a-b5eb-373870ca27ce",
                "name": "Movie",
                "description": None,
                "is_active": True,
                "created_at": mock_create_use_case.execute.return_value.created_at,
            },
        )

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
            **{**self.__init_all_none(), "list_use_case": lambda: mock_list_use_case}
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
                        "created_at": mock_list_use_case.execute.return_value.items[0].created_at,
                    },
                ],
                "total": 1,
                "current_page": 1,
                "per_page": 2,
                "last_page": 1
            },
        )
