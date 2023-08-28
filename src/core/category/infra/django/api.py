from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from core.category.application.use_cases import CreateCategoryUseCase
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from dataclasses import asdict

@api_view(['POST'])
def hello_world(request: Request):
    create_use_case = CreateCategoryUseCase(CategoryInMemoryRepository())
    input_param = CreateCategoryUseCase.Input(name=request.data['name'])
    output = create_use_case.execute(input_param)
    return Response(asdict(output))