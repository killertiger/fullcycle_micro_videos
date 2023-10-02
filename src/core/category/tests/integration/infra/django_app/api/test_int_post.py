import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django_app import container
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.tests.fixture.categories_api_fixture import (
    CreateCategoryAPIFixture,
    HttpExpect,
)
from core.category.tests.helpers import init_category_resource_all_none
from core.__seedwork.infra.testing.helpers import assert_response_data, make_request


@pytest.mark.django_db
class TestCategoryResourcePostMethodInt:
    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.resource = CategoryResource(
            **{
                **init_category_resource_all_none(),
                'create_use_case': container.use_case_category_create_category,
            }
        )

    @pytest.mark.parametrize('http_expect', CreateCategoryAPIFixture.arrange_for_invalid_requests())
    def test_validation_errors(self, http_expect: HttpExpect):
        request = make_request(http_method='post', send_data=http_expect.request.body)

        with pytest.raises(http_expect.exception.__class__) as assert_exception:
            self.resource.post(request)

        assert assert_exception.value.detail == http_expect.exception.detail

    @pytest.mark.parametrize('http_expect', CreateCategoryAPIFixture.arrange_for_save())
    def test_method_post(self, http_expect: HttpExpect):
        request = make_request(http_method='post', send_data=http_expect.request.body)
        response = self.resource.post(request)
        assert response.status_code == 201
        assert CreateCategoryAPIFixture.keys_in_category_response() == list(
            response.data.keys()
        )

        category_created = self.repo.find_by_id(response.data['id'])
        serialized = CategoryResource.category_to_response(category_created)
        assert response.data == serialized

        assert_response_data(response.data, http_expect.response.body)