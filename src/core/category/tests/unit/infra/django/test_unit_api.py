from datetime import datetime
import unittest
from unittest import mock
from core.category.application.use_cases import (
    CreateCategoryUseCase
)
from core.category.infra.django.api import CategoryResource
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

class TestCategoryResourceUnit(unittest.TestCase):
    def test_post_method(self):
        send_data = {'name': 'fake name'}
        mock_create_use_case = mock.Mock(CreateCategoryUseCase)
        
        mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
            id='fc98cf57-4615-4b0a-b5eb-373870ca27ce',
            name='Movie',
            description=None,
            is_active=True,
            created_at=datetime.now()
        )
        
        resource = CategoryResource(
            list_use_case=None,
            create_use_case=lambda: mock_create_use_case
        )
        
        _request = APIRequestFactory().post('', send_data)
        request = Request(_request)
        request._full_data = send_data
        
        response = resource.post(request)
        
        mock_create_use_case.execute.assert_called_with(CreateCategoryUseCase.Input(
            name='fake name'
        ))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            'id': 'fc98cf57-4615-4b0a-b5eb-373870ca27ce',
            'name':'Movie',
            'description': None,
            'is_active': True,
            'created_at': mock_create_use_case.execute.return_value.created_at
        })