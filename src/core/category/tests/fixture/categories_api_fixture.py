from typing import Any, Optional
from dataclasses import dataclass
import pytest
from rest_framework.exceptions import ValidationError, ErrorDetail
from core.category.domain.entities import Category
from core.__seedwork.domain.exceptions import EntityValidationException


@dataclass
class Request:
    body: Any


@dataclass
class Response:
    body: Any


@dataclass
class HttpExpect:
    request: Request
    response: Optional[Response] = None
    exception: Optional[Exception] = None


@dataclass
class CategoryInvalidBodyFixture:
    body_empty: HttpExpect
    name_none: HttpExpect
    name_empty: HttpExpect
    name_not_a_str: HttpExpect
    description_not_a_str: HttpExpect
    is_active_none: HttpExpect
    is_active_empty: HttpExpect
    is_active_not_a_bool: HttpExpect

    @staticmethod
    def arrange():
        faker = Category.fake().a_category()

        return CategoryInvalidBodyFixture(
            body_empty=HttpExpect(
                request=Request(body={}),
                exception=ValidationError(
                    {'name': [ErrorDetail('This field is required.', 'required')]}
                ),
            ),
            name_none=HttpExpect(
                request=Request(body={'name': faker.with_invalid_name_none().name}),
                exception=ValidationError(
                    {'name': [ErrorDetail('This field may not be null.', 'null')]}
                ),
            ),
            name_empty=HttpExpect(
                request=Request(body={'name': faker.with_invalid_name_empty().name}),
                exception=ValidationError(
                    {'name': [ErrorDetail('This field may not be blank.', 'blank')]}
                ),
            ),
            name_not_a_str=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_not_string().name}
                ),
                exception=ValidationError(
                    {'name': [ErrorDetail('Not a valid string.', 'invalid')]}
                ),
            ),
            description_not_a_str=HttpExpect(
                request=Request(
                    body={
                        'description': faker.with_invalid_description_not_string().description
                    }
                ),
                exception=ValidationError(
                    {
                        'name': [ErrorDetail('This field is required.', 'required')],
                        'description': [ErrorDetail('Not a valid string.', 'invalid')],
                    }
                ),
            ),
            is_active_none=HttpExpect(
                request=Request(
                    body={'is_active': faker.with_invalid_is_active_none().is_active}
                ),
                exception=ValidationError(
                    {
                        'name': [ErrorDetail('This field is required.', 'required')],
                        'is_active': [
                            ErrorDetail('This field may not be null.', 'null')
                        ],
                    }
                ),
            ),
            is_active_empty=HttpExpect(
                request=Request(
                    body={'is_active': faker.with_invalid_is_active_empty().is_active}
                ),
                exception=ValidationError(
                    {
                        'name': [ErrorDetail('This field is required.', 'required')],
                        'is_active': [
                            ErrorDetail('Must be a valid boolean.', 'invalid')
                        ],
                    }
                ),
            ),
            is_active_not_a_bool=HttpExpect(
                request=Request(
                    body={
                        'is_active': faker.with_invalid_is_active_not_boolean().is_active
                    }
                ),
                exception=ValidationError(
                    {
                        'name': [ErrorDetail('This field is required.', 'required')],
                        'is_active': [
                            ErrorDetail('Must be a valid boolean.', 'invalid')
                        ],
                    }
                ),
            ),
        )


@dataclass
class CategoryEntityValidationErrorFixture:
    name_none: HttpExpect
    name_empty: HttpExpect
    name_not_a_str: HttpExpect
    name_too_long: HttpExpect
    description_not_a_str: HttpExpect
    is_active_none: HttpExpect
    is_active_empty: HttpExpect
    is_active_not_a_bool: HttpExpect

    def arrange():
        faker = Category.fake().a_category()

        return CategoryEntityValidationErrorFixture(
            name_none=HttpExpect(
                request=Request(body={'name': faker.with_invalid_name_none().name}),
                exception=EntityValidationException(
                    {'name': ['This field may not be null.']}
                ),
            ),
            name_empty=HttpExpect(
                request=Request(body={'name': faker.with_invalid_name_empty().name}),
                exception=EntityValidationException(
                    {'name': ['This field may not be blank.']}
                ),
            ),
            name_not_a_str=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_not_string().name}
                ),
                exception=EntityValidationException({'name': ['Not a valid string.']}),
            ),
            name_too_long=HttpExpect(
                request=Request(body={'name': faker.with_invalid_name_too_long().name}),
                exception=EntityValidationException(
                    {'name': ['Ensure this field has no more than 255 characters.']}
                ),
            ),
            description_not_a_str=HttpExpect(
                request=Request(
                    body={
                        'name': faker.with_invalid_name_none().name,
                        'description': faker.with_invalid_description_not_string().description,
                    }
                ),
                exception=EntityValidationException(
                    {
                        'name': ['This field may not be null.'],
                        'description': ['Not a valid string.'],
                    }
                ),
            ),
            is_active_none=HttpExpect(
                request=Request(
                    body={
                        'name': faker.with_invalid_name_none().name,
                        'is_active': faker.with_invalid_is_active_none().is_active,
                    }
                ),
                exception=EntityValidationException(
                    {
                        'name': ['This field may not be null.'],
                        'is_active': ['This field may not be null.'],
                    }
                ),
            ),
            is_active_empty=HttpExpect(
                request=Request(
                    body={
                        'name': faker.with_invalid_name_none().name,
                        'is_active': faker.with_invalid_is_active_empty().is_active,
                    }
                ),
                exception=EntityValidationException(
                    {
                        'name': ['This field may not be null.'],
                        'is_active': ['Must be a valid boolean.'],
                    }
                ),
            ),
            is_active_not_a_bool=HttpExpect(
                request=Request(
                    body={
                        'name': faker.with_invalid_name_none().name,
                        'is_active': faker.with_invalid_is_active_not_boolean().is_active,
                    }
                ),
                exception=EntityValidationException(
                    {
                        'name': ['This field may not be null.'],
                        'is_active': ['Must be a valid boolean.'],
                    }
                ),
            ),
        )


class CategoryAPIFixture:
    @staticmethod
    def keys_in_category_response():
        return ['id', 'name', 'description', 'is_active', 'created_at']


class CreateCategoryAPIFixture:
    @staticmethod
    def arrange_for_invalid_requests():
        fixture = CategoryInvalidBodyFixture.arrange()
        return [
            pytest.param(fixture.body_empty, id='body_empty'),
            pytest.param(fixture.name_none, id='name_none'),
            pytest.param(fixture.name_empty, id='name_empty'),
            pytest.param(fixture.is_active_none, id='is_active_none'),
            pytest.param(fixture.is_active_empty, id='is_active_empty'),
            pytest.param(fixture.is_active_not_a_bool, id='is_active_not_a_bool'),
        ]

    @staticmethod
    def arrange_for_entity_validation_errors():
        fixture = CategoryEntityValidationErrorFixture.arrange()
        return [
            pytest.param(fixture.name_none, id='name_none'),
            pytest.param(fixture.name_empty, id='name_empty'),
            pytest.param(fixture.name_not_a_str, id='name_not_a_str'),
            pytest.param(fixture.name_too_long, id='name_too_long'),
            pytest.param(fixture.description_not_a_str, id='description_not_a_str'),
            pytest.param(fixture.is_active_none, id='is_active_none'),
            pytest.param(fixture.is_active_empty, id='is_active_empty'),
            pytest.param(fixture.is_active_not_a_bool, id='is_active_not_a_bool'),
        ]

    @staticmethod
    def keys_in_category_response():
        return CategoryAPIFixture.keys_in_category_response()

    @staticmethod
    def arrange_for_save():
        faker = (
            Category.fake()
            .a_category()
            .with_name('Movie')
            .with_description('description test')
        )

        data = [
            HttpExpect(
                request=Request(
                    body={
                        'name': faker.name,
                    }
                ),
                response=Response(
                    body={'name': faker.name, 'description': None, 'is_active': True}
                ),
            ),
            HttpExpect(
                request=Request(
                    body={
                        'name': faker.name,
                        'description': faker.description,
                    }
                ),
                response=Response(
                    body={
                        'name': faker.name,
                        'description': faker.description,
                        'is_active': True,
                    }
                ),
            ),
        ]

        return [pytest.param(item, id=str(item.request.body)) for item in data]


class UpdateCategoryAPIFixture:
    @staticmethod
    def arrange_for_invalid_requests():
        fixture = CategoryInvalidBodyFixture.arrange()
        return [
            pytest.param(fixture.body_empty, id='body_empty'),
            pytest.param(fixture.name_none, id='name_none'),
            pytest.param(fixture.name_empty, id='name_empty'),
            pytest.param(fixture.is_active_none, id='is_active_none'),
            pytest.param(fixture.is_active_empty, id='is_active_empty'),
            pytest.param(fixture.is_active_not_a_bool, id='is_active_not_a_bool'),
        ]

    @staticmethod
    def arrange_for_entity_validation_errors():
        fixture = CategoryEntityValidationErrorFixture.arrange()
        return [
            pytest.param(fixture.name_none, id='name_none'),
            pytest.param(fixture.name_empty, id='name_empty'),
            pytest.param(fixture.name_not_a_str, id='name_not_a_str'),
            pytest.param(fixture.name_too_long, id='name_too_long'),
            pytest.param(fixture.description_not_a_str, id='description_not_a_str'),
        ]

    @staticmethod
    def keys_in_category_response():
        return CategoryAPIFixture.keys_in_category_response()

    @staticmethod
    def arrange_for_save():
        data = [
            HttpExpect(
                request=Request(
                    body={
                        'name': 'Movie',
                    }
                ),
                response=Response(
                    body={
                        'name': 'Movie',
                        'description': None,
                        'is_active': True,
                    }
                ),
            ),
            HttpExpect(
                request=Request(
                    body={'name': 'Movie', 'description': 'test description'}
                ),
                response=Response(
                    body={
                        'name': 'Movie',
                        'description': 'test description',
                        'is_active': True,
                    }
                ),
            ),
            HttpExpect(
                request=Request(body={'name': 'Movie', 'is_active': False}),
                response=Response(
                    body={
                        'name': 'Movie',
                        'description': None,
                        'is_active': False,
                    }
                ),
            ),
            HttpExpect(
                request=Request(body={'name': 'Movie', 'is_active': True}),
                response=Response(
                    body={
                        'name': 'Movie',
                        'description': None,
                        'is_active': True,
                    }
                ),
            ),
        ]

        return [pytest.param(item, id=str(item.request.body)) for item in data]
