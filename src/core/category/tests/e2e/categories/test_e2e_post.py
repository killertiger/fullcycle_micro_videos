import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.tests.fixture.categories_api_fixture import CreateCategoryAPIFixture, HttpExpect
from django_app import container

@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoriesPostE2E:
    
    client_http: APIClient
    category_repository: CategoryRepository
    
    @classmethod
    def setup_class(cls):
        cls.client_http  = APIClient()
        cls.category_repository = container.repository_category_django_orm()
    
    @pytest.mark.parametrize(
        'http_expect', CreateCategoryAPIFixture.arrange_for_invalid_requests()
    )
    def test_invalid_request(self, http_expect: HttpExpect):
        response: Response = self.client_http.post('/categories/', data=http_expect.request.body, format='json')

        assert response.status_code == 400
        assert response.content == JSONRenderer().render(http_expect.exception.detail)
    
    
    @pytest.mark.parametrize('http_expect', CreateCategoryAPIFixture.arrange_for_save())
    def test_post(self, http_expect: HttpExpect):
        response: Response = self.client_http.post('/categories/', data=http_expect.request.body, format='json')
        assert response.status_code == 201
        
        assert 'data' in response.data
        
        response_data = response.data['data']
        assert list(response_data.keys()) == CreateCategoryAPIFixture.keys_in_category_response()
        
        category_created = self.category_repository.find_by_id(response_data['id'])
        serialized = CategoryResource.category_to_response(category_created)
        assert response.data == serialized
        
        assert response.data == {
            'data': {
                **http_expect.response.body,
                'id': category_created.id,
                'created_at': serialized['data']['created_at'],
            }
        }