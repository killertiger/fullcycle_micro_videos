from typing import Any, Optional
from dataclasses import dataclass
import pytest
from rest_framework.exceptions import ValidationError, ErrorDetail
from core.category.domain.entities import Category


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
    name_empty: HttpExpect
    name_none: HttpExpect
    name_not_a_str: HttpExpect
    description_not_a_str: HttpExpect
    is_active_empty: HttpExpect
    is_active_not_a_bool: HttpExpect

    @staticmethod
    def arrange():
        faker=Category.fake().a_category()
            
        return CategoryInvalidBodyFixture(
            

            body_empty=HttpExpect(
                request=Request(body={}),
                exception=ValidationError({
                    'name': [ErrorDetail('This field is required.', 'required')]
                })
            ),
            name_empty=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_empty().name}
                ),
                exception=ValidationError({
                    'name': [ErrorDetail('This may not be blank.', 'blank')]
                })
            ),
            name_none=HttpExpect(
                request=Request(body={'name': faker.with_invalid_name_none().name}),
                exception=ValidationError({
                    'name': [ErrorDetail('This field is required.', 'required')]
                })
            ),
            name_not_a_str=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_not_string().name}
                ),
                exception=ValidationError({
                    'name': [ErrorDetail('Not a valid string.', 'invalid')]
                })
            ),
            description_not_a_str=HttpExpect(
                request=Request(
                    body={'description': faker.with_invalid_description_not_string().description}
                ),
                exception=ValidationError({
                    'name': [ErrorDetail('This field is required.', 'required')],
                    'description': [ErrorDetail('Not a valid string.', 'invalid')]
                })
            ),
            is_active_empty=HttpExpect(
                request=Request(
                        body={'is_active': faker.with_invalid_is_active_empty().is_activeÍ}
                    ),
                exception=ValidationError({
                    'name': [ErrorDetail('This field is required.', 'required')],
                    'is_active': [ErrorDetail('Must be a valid boolean.', 'invalid')]
                })
            ),
            is_active_not_a_bool=HttpExpect(
                request=Request(
                        body={'is_active': faker.with_invalid_is_active_not_boolean().is_activeÍ}
                    ),
                exception=ValidationError({
                    'name': [ErrorDetail('This field is required.', 'required')],
                    'is_active': [ErrorDetail('Must be a valid boolean.', 'invalid')]
                })
            ),
        )


class CategoryAPIFixture:
    @staticmethod
    def keys_in_category_response():
        return ['id', 'name', 'description', 'is_active', 'created_at']

    @staticmethod
    def arrange_for_save():
        faker = Category.fake().a_category()\
            .with_name('Movie')\
            .with_description('description test')

        data = [
            HttpExpect(
                request=Request(
                    body={
                        'name': faker.name,
                    }
                ),
                response=Response(
                    body={'description': None, 'is_active': True}),
            ),
            HttpExpect(
                request=Request(
                    body={'name': faker.name, 'description': faker.description}
                ),
                response=Response(body={'is_active': True}),
            ),
        ]

        return [pytest.param(item, id=str(item.request.body)) for item in data]
