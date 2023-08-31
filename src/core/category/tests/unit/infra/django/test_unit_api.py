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
        create_use_case = mock.Mock(CreateCategoryUseCase)
        
        resource = CategoryResource(
            list_use_case=None,
            create_use_case=lambda: create_use_case
        )
        
        send_data = {'name': 'fake name'}
        _request = APIRequestFactory().post('', send_data)
        request = Request(_request)
        request._full_data = send_data
        
        try:
            response = resource.post(request)
        except:
            create_use_case.execute.assert_called()