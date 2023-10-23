from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from .cast_member_django_app.repositories import CastMemberDjangoRepository
from .in_memory.repositories import CastMemberInMemoryRepository
from core.cast_member.application.use_cases import CreateCastMemberUseCase, DeleteCastMemberUseCase, ListCastMemberUseCase, GetCastMemberUseCase, UpdateCastMemberUseCase

class CastMemberContainer(DeclarativeContainer):
    cast_member_repository_in_memory = providers.Singleton(CastMemberInMemoryRepository)
    
    cast_member_repository_django_orm = providers.Singleton(CastMemberDjangoRepository)
    
    use_case_list_cast_members = providers.Singleton(ListCastMemberUseCase, cast_member_repo=cast_member_repository_django_orm)
    
    use_case_get_cast_member = providers.Singleton(GetCastMemberUseCase, cast_member_repo=cast_member_repository_django_orm)
    
    use_case_create_cast_member = providers.Singleton(CreateCastMemberUseCase, cast_member_repo=cast_member_repository_django_orm)
    
    use_case_update_cast_member = providers.Singleton(UpdateCastMemberUseCase, cast_member_repo=cast_member_repository_django_orm)
    
    use_case_delete_cast_member = providers.Singleton(DeleteCastMemberUseCase, cast_member_repo=cast_member_repository_django_orm)