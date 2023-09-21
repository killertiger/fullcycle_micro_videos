import pytest
from django_app import container
from rest_framework.exceptions import (ValidationError, ErrorDetail)
from core.category.domain.entities import Category
from core.__seedwork.domain.exceptions import NotFoundException
from core.category.infra.django_app.api import CategoryResource
from core.category.infra.django_app.repositories import CategoryRepository
from core.category.tests.helpers import init_category_resource_all_none
from core.category.tests.fixture.categories_api_fixture import CategoryAPIFixture


@pytest.mark.django_db
class TestCategoryResourceGetObjectMethodInt:
    
    resource: CategoryResource
    repo: CategoryRepository
    
    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.resource = CategoryResource(**{
            **init_category_resource_all_none(),
            'get_use_case': container.use_case_category_get_category
        })
    
    def test_throw_exception_when_uuid_is_valid(self):
        with pytest.raises(NotFoundException) as assert_exception:
            self.resource.get_object(id='fake id')
            
        assert assert_exception.value.detail == {
            'id': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]
        }
        
    def test_throw_exception_when_category_not_found(self):
        uuid_value = 'ab368028-9fc3-4eae-810c-3735af62d6f2'
        with pytest.raises(NotFoundException) as assert_exception:
            self.resource.get_object(id=uuid_value)
        assert assert_exception.value.args[0] == f"Entity not found using ID '{uuid_value}'"
        
        
    def test_get_object_method(self):
        category = Category(name='movie')
        self.repo.insert(category)
        
        response = self.resource.get_object(category.id)
        
        assert response.status_code == 200
        serialized = CategoryResource.category_to_response(category)
        assert CategoryAPIFixture.keys_in_category_response() == list(response.data.keys())
        assert response.data == serialized
        
        assert response.data == {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'is_active': category.is_active,
            'created_at': serialized['created_at']
        }
    