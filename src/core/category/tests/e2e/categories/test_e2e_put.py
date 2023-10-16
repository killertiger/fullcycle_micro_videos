from unittest.mock import patch, PropertyMock
from core.category.domain.entities import Category
import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.infra.django_app.serializer import CategorySerializer
from core.category.tests.fixture.categories_api_fixture import UpdateCategoryAPIFixture, HttpExpect
from django_app import container

@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoriesPutE2E:
    
    client_http: APIClient
    category_repository: CategoryRepository
    
    @classmethod
    def setup_class(cls):
        cls.client_http  = APIClient()
        cls.category_repository = container.repository_category_django_orm()
    
    @pytest.mark.parametrize(
        'http_expect', UpdateCategoryAPIFixture.arrange_for_invalid_requests()
    )
    def test_invalid_request(self, http_expect: HttpExpect):
        unique_id = UniqueEntityId().id
        response: Response = self.client_http.put(f'/categories/{unique_id}/', data=http_expect.request.body, format='json')

        assert response.status_code == 422
        assert response.content == JSONRenderer().render(http_expect.exception.detail)
    
    @pytest.mark.parametrize(
        'http_expect', UpdateCategoryAPIFixture.arrange_for_entity_validation_errors()
    )
    def test_entity_validation_error(self, http_expect: HttpExpect):
        with (
            patch.object(CategorySerializer, 'is_valid') as mock_is_valid,
            patch.object(
                CategorySerializer,
                'validated_data',
                new_callable=PropertyMock,
                return_value=http_expect.request.body,
            ) as mock_validated_data,
        ):
            category = Category.fake().a_category().build()
            self.category_repository.insert(category)
            
            response: Response = self.client_http.put(f'/categories/{category.id}/', data=http_expect.request.body, format='json')

            mock_is_valid.assert_called()
            mock_validated_data.assert_called()

            assert response.status_code == 422
            assert response.content == JSONRenderer().render(http_expect.exception.error)
    
    
    @pytest.mark.parametrize('http_expect', UpdateCategoryAPIFixture.arrange_for_save())
    def test_put(self, http_expect: HttpExpect):
        category_created = Category.fake().a_category().build()
        self.category_repository.insert(category_created)
        
        response: Response = self.client_http.put(f'/categories/{category_created.id}/', data=http_expect.request.body, format='json')
        assert response.status_code == 200
        
        assert 'data' in response.data
        
        response_data = response.data['data']
        assert list(response_data.keys()) == UpdateCategoryAPIFixture.keys_in_category_response()
        
        category_updated = self.category_repository.find_by_id(response_data['id'])
        serialized = CategoryResource.category_to_response(category_updated)
        assert response.data == serialized
        
        assert response.data == {
            'data': {
                **http_expect.response.body,
                'id': category_updated.id,
                'created_at': serialized['data']['created_at'],
            }
        }