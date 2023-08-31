from typing import Callable
from dataclasses import asdict, dataclass
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status as http_status
from core.category.application.use_cases import (CreateCategoryUseCase, 
                                                 ListCategoriesUseCase
                                                 )


@dataclass(slots=True)
class CategoryResource(APIView):
    
    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    
    def post(self, request: Request):
        print(request.data)
        input_param = CreateCategoryUseCase.Input(**request.data)
        output = self.create_use_case().execute(input_param)
        return Response(asdict(output), http_status.HTTP_201_CREATED)
    
    def get(self, request: Request):
        print(request.data)
        input_param = ListCategoriesUseCase.Input(**request.query_params.dict())
        output = self.list_use_case().execute(input_param)
        return Response(asdict(output))
