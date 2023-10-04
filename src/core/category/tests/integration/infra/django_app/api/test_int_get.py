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
class TestCategoryResourceGetMethodInt:
    
    resource: CategoryResource
    repo: CategoryRepository
    
    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.resource = CategoryResource(**{
            **init_category_resource_all_none(),
            'list_use_case': container.use_case_category_list_categories
        })
    
    def test_execute_using_empty_search_params(self):
        pass
    
    def test_execute_using_pagination_and_sort_and_filter(self):
        pass