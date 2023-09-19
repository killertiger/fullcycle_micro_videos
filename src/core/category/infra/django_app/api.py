from typing import Callable
from dataclasses import asdict, dataclass
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status as http_status
from core.category.application.dto import CategoryOutput
from core.category.infra.django_app.serializer import CategorySerializer
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase,
)


@dataclass(slots=True)
class CategoryResource(APIView):
    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]
    update_use_case: Callable[[], UpdateCategoryUseCase]
    delete_use_case: Callable[[], DeleteCategoryUseCase]

    def post(self, request: Request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_param = CreateCategoryUseCase.Input(**serializer.validated_data)
        output = self.create_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        
        return Response(body, http_status.HTTP_201_CREATED)

    def get(self, request: Request, id: str = None):
        if id:
            return self.get_object(id)

        input_param = ListCategoriesUseCase.Input(**request.query_params.dict())
        output = self.list_use_case().execute(input_param)
        return Response(asdict(output))

    def get_object(self, id: str):
        input_param = GetCategoryUseCase.Input(id)
        output = self.get_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        
        return Response(body, http_status.HTTP_201_CREATED)


    def put(self, request: Request, id: str):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_param = UpdateCategoryUseCase.Input(
            **{'id': id, **serializer.validated_data}
        )
        output = self.update_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        
        return Response(body, http_status.HTTP_201_CREATED)


    def delete(self, _request: Request, id: str):
        input_param = DeleteCategoryUseCase.Input(id=id)
        self.delete_use_case().execute(input_param)

        return Response(status=http_status.HTTP_204_NO_CONTENT)
    
    @staticmethod
    def category_to_response(category: CategoryOutput):
        serializer = CategorySerializer(instance= category)
        return serializer.data
