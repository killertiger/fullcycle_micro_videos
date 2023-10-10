import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response

@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoriesPostE2E:
    def test_post(self):
        client_http = APIClient()
        response: Response = client_http.post('/categories/', data={'name': 'test'})
        assert response.status_code == 201
        