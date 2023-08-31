from django.contrib import admin
from django.urls import path
from core.category.application.use_cases import CreateCategoryUseCase

from core.category.infra.django.api import CategoryResource
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from django_app import container


# class CategoryInMemoryRepositoryFactory:
    
#     repo: CategoryInMemoryRepository = None
    
#     @classmethod
#     def create(cls):
#         if not cls.repo:
#             cls.repo = CategoryInMemoryRepository()
#         return cls.repo

# class CreateCategoryUseCaseFactory:
#     @staticmethod
#     def create():
#         repo = CategoryInMemoryRepositoryFactory.create()
#         return CreateCategoryUseCase(repo)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', CategoryResource.as_view(
                create_use_case = container.use_case_category_create_category,
                list_use_case = container.use_case_category_list_category,
            )
         ),
]
