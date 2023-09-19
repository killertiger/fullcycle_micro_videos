from dependency_injector import containers, providers
from core.category.infra.django_app.repositories import CategoryDjangoRepository
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase,
)


class Container(containers.DeclarativeContainer):
    repository_category_django_orm = providers.Singleton(CategoryDjangoRepository)

    use_case_category_create_category = providers.Singleton(
        CreateCategoryUseCase, category_repo=repository_category_django_orm
    )
    use_case_category_list_categories = providers.Singleton(
        ListCategoriesUseCase, category_repo=repository_category_django_orm
    )
    use_case_category_get_category = providers.Singleton(
        GetCategoryUseCase, category_repo=repository_category_django_orm
    )
    use_case_category_update_category = providers.Singleton(
        UpdateCategoryUseCase, category_repo=repository_category_django_orm
    )
    use_case_category_delete_category = providers.Singleton(
        DeleteCategoryUseCase, category_repo=repository_category_django_orm
    )
