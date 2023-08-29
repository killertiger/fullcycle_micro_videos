from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from core.category.application.use_cases import CreateCategoryUseCase, ListCategoriesUseCase
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from dataclasses import asdict

class CategoryResource(APIView):
    
    repo = CategoryInMemoryRepository()
    
    def post(self, request: Request):
        create_use_case = CreateCategoryUseCase(self.repo)
        print(request.data)
        input_param = CreateCategoryUseCase.Input(name=request.data['name'])
        output = create_use_case.execute(input_param)
        return Response(asdict(output))
    
    def get(self, request: Request):
        list_use_case = ListCategoriesUseCase(self.repo)
        print(request.data)
        input_param = ListCategoriesUseCase.Input()
        output = list_use_case.execute(input_param)
        return Response(asdict(output))

# @api_view(['POST'])
# def hello_world(request: Request):
#     create_use_case = CreateCategoryUseCase(CategoryInMemoryRepository())
#     input_param = CreateCategoryUseCase.Input(name=request.data['name'])
#     output = create_use_case.execute(input_param)
#     return Response(asdict(output))