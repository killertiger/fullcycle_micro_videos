from dataclasses import asdict, dataclass
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from core.category.application.use_cases import CreateCategoryUseCase, ListCategoriesUseCase
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository



@dataclass(slots=True)
class CategoryResource(APIView):
    
    # repo = CategoryInMemoryRepository()
    create_use_case: CreateCategoryUseCase
    
    def post(self, request: Request):
        # create_use_case = CreateCategoryUseCaseFactory.create()
        print(request.data)
        input_param = CreateCategoryUseCase.Input(name=request.data['name'])
        output = self.create_use_case.execute(input_param)
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