import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.infra.django_app.models import CategoryModel
from core.category.infra.django_app.repositories import CategoryDjangoRepository
from core.category.tests.fixture.categories_api_fixture import (
    CategoryAPIFixture,
    HttpExpect,
)
from django_app import container

@pytest.mark.django_db
class TestCategoryResourcePostMethodInt:
    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        # cls.repo = CategoryDjangoRepository()
        cls.repo = container.repository_category_in_memory()
        cls.resource = CategoryResource(
            create_use_case=container.use_case_category_create_category,
            update_use_case=None,
            get_use_case=None,
            list_use_case=None,
            delete_use_case=None,
        )

    @pytest.mark.parametrize('http_expect', CategoryAPIFixture.arrange_for_save())
    def test_method_post(self, http_expect: HttpExpect):
        request_factory = APIRequestFactory()
        _request = request_factory.get('/categories')
        request = Request(_request) 
        request._full_data = http_expect.request.body
        response = self.resource.post(request)
        assert response.status_code == 201
        assert CategoryAPIFixture.keys_in_category_response() == list(response.data.keys())
        
        category_created = self.repo.find_by_id(response.data['id'])
        assert response.data == {
            'id': category_created.id,
            'name': category_created.name,
            'description': category_created.description,
            'is_active': category_created.is_active,
            'created_at': category_created.created_at
        }
        
        expected_data = {**http_expect.request.body, **http_expect.response.body}
        for key, value in expected_data.items():
            assert response.data[key] == value
            
