from core.category.domain.entities import Category
from core.category.infra.django_app.serializer import CategorySerializer
import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django_app import container
from unittest.mock import patch, PropertyMock
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.tests.fixture.categories_api_fixture import (
    UpdateCategoryAPIFixture,
    HttpExpect,
)
from core.category.tests.helpers import init_category_resource_all_none
from core.__seedwork.infra.testing.helpers import assert_response_data, make_request


@pytest.mark.django_db
class TestCategoryResourcePutMethodInt:
    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.resource = CategoryResource(
            **{
                **init_category_resource_all_none(),
                'update_use_case': container.use_case_category_update_category,
            }
        )

    @pytest.mark.parametrize(
        'http_expect', UpdateCategoryAPIFixture.arrange_for_invalid_requests()
    )
    def test_invalid_request(self, http_expect: HttpExpect):
        uuid_value = 'ac8134ce-a15f-4517-9849-3b53b5f3972d'
        request = make_request(http_method='put', send_data=http_expect.request.body)

        with pytest.raises(http_expect.exception.__class__) as assert_exception:
            self.resource.put(request, uuid_value)

        assert assert_exception.value.detail == http_expect.exception.detail

    @pytest.mark.parametrize(
        'http_expect', UpdateCategoryAPIFixture.arrange_for_entity_validation_errors()
    )
    def test_entity_validation_error(self, http_expect: HttpExpect):
        category = Category.fake().a_category().build()
        self.repo.insert(category)
        
        with (
            patch.object(CategorySerializer, 'is_valid') as mock_is_valid,
            patch.object(
                CategorySerializer,
                'validated_data',
                new_callable=PropertyMock,
                return_value=http_expect.request.body,
            ) as mock_validated_data,
        ):
            request = make_request(
                http_method='put', send_data=http_expect.request.body
            )

            with pytest.raises(http_expect.exception.__class__) as assert_exception:
                self.resource.put(request, category.id)
            mock_is_valid.assert_called()
            mock_validated_data.assert_called()
            assert assert_exception.value.error == http_expect.exception.error

    @pytest.mark.parametrize('http_expect', UpdateCategoryAPIFixture.arrange_for_save())
    def test_method_put(self, http_expect: HttpExpect):
        request = make_request(http_method='put', send_data=http_expect.request.body)
        response = self.resource.put(request)
        assert response.status_code == 201
        assert UpdateCategoryAPIFixture.keys_in_category_response() == list(
            response.data.keys()
        )

        category_created = self.repo.find_by_id(response.data['id'])
        serialized = CategoryResource.category_to_response(category_created)
        assert response.data == serialized

        assert_response_data(response.data, http_expect.response.body)
