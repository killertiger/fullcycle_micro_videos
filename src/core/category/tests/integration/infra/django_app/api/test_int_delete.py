import pytest
from django_app import container
from rest_framework.exceptions import ErrorDetail, ValidationError
from core.category.domain.entities import Category
from core.__seedwork.domain.exceptions import NotFoundException
from core.category.domain.repositories import CategoryRepository
from core.category.infra.category_django_app.api import CategoryResource
from core.category.tests.helpers import init_category_resource_all_none
from core.__seedwork.infra.testing.helpers import make_request


@pytest.mark.django_db
class TestCategoryResourceDeleteMethodInt:
    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.resource = CategoryResource(
        **{
                **init_category_resource_all_none(),
                'delete_use_case': container.use_case_category_delete_category,
            }
        )

    def test_throw_exception_when_uuid_is_valid(self):
        request = make_request(http_method='delete')

        with pytest.raises(ValidationError) as assert_exception:
            self.resource.delete(request, 'fake id')

        assert assert_exception.value.detail == {
            'id': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]
        }

    def test_throw_exception_when_category_not_found(self):
        uuid_value = 'ab368028-9fc3-4eae-810c-3735af62d6f2'
        request = make_request(http_method='delete')
        with pytest.raises(NotFoundException) as assert_exception:
            self.resource.delete(request, id=uuid_value)
        assert (
            assert_exception.value.args[0]
            == f"Entity not found using ID '{uuid_value}'"
        )

    def test_method_delete(self):
        category = Category.fake().a_category().build()
        self.repo.insert(category)

        request = make_request(http_method='delete')
        response = self.resource.delete(request, category.id)
        assert response.status_code == 204

        with pytest.raises(NotFoundException) as assert_exception:
            self.repo.find_by_id(category.id)

        assert (
            assert_exception.value.args[0]
            == f"Entity not found using ID '{category.id}'"
        )
