import pytest
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.infra.django_app.models import CategoryModel
from core.category.infra.django_app.repositories import CategoryDjangoRepository


@pytest.mark.django_db
class TestCategoryResourcePostMethodInt:
    resource: CategoryResource
    repo: CategoryRepository
    
    @classmethod
    def setup_class(cls):
        cls.repo = CategoryDjangoRepository()
        cls.resource = CategoryResource(
            create_use_case=None,
            update_use_case=None,
            get_use_case=None,
            list_use_case=None,
            delete_use_case=None,
        )
        
