from itertools import count
from typing import TYPE_CHECKING, List, Type
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.repositories import SortDirection
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.cast_member.domain.repositories import CastMemberRepository
from core.cast_member.domain.entities import CastMember
from core.cast_member.infra.cast_member_django_app.mappers import CastMemberModelMapper
from django.core.paginator import Paginator


if TYPE_CHECKING:
    from core.cast_member.infra.cast_member_django_app.models import CastMemberModel
    
class CastMemberDjangoRepository(CastMemberRepository):
    
    sortable_fields: List[str] = ['name', 'created_at']
    model: Type['CastMemberModel']
    
    def __init__(self) -> None:
        from core.cast_member.infra.cast_member_django_app.models import CastMemberModel
        self.model = CastMemberModel
    
    def insert(self, entity: CastMember) -> None:
        model = CastMemberModelMapper.to_model(entity)
        model.save()
        
    def bullk_insert(self, entities: List[CastMember]) -> None:
        self.model.objects.bulk_create(
            list(
                map(
                    CastMemberModelMapper.to_model, entities
                )
            )
        )
    
    def find_by_id(self, entity_id: str | UniqueEntityId) -> CastMember:
        id_str = str(entity_id)
        model = self._get(id_str)
        return CastMemberModelMapper.to_entity(model)
    
    def find_all(self) -> List[CastMember]:
        return [CastMemberModelMapper.to_entity(model) for model in self.model.objects.all()]
    
    def update(self, entity: CastMember) -> None:
        self._get(entity.id)
        model = CastMemberModelMapper.to_model(entity)
        model.save()
        
    def delete(self, entity_id: str) -> None:
        try:
            return self.model.objects.get(pk=entity_id)
        except(self.model.DoesNotExist, django_exceptions.ValidationError) as exception:
            raise NotFoundException(
                f"Entity not found using ID '{entity_id}'"
            ) from exception
            
    def search(self, input_params: CastMemberRepository.SearchParams) -> CastMemberRepository.SearchResult:
        query = self.model.objects.all()
        
        if input_params.filter:
            if 'name' in input_params.filter:
                query = query.filter(name__icontains=input_params.filter['name'])
            if 'cast_member_type' in input_params.filter:
                query = query.filter(cast_member_type=input_params.filter['cast_member_type'].value.value)
        if input_params.sort and input_params.sort in self.sortable_fields:
            query = query.order_by(
                input_params.sort if input_params.sort_dir == SortDirection.ASC else f'-{input_params.sort}'
            )
        else:
            query = query.order_by('-created_at')
            
        paginator = Paginator(query, input_params.per_page)
        page_obj = paginator.page(input_params.page)
        
        return CastMemberRepository.SearchResult(
            items=[CastMemberModelMapper.to_entity(model) for model in page_obj.object_list]
            total=paginator.count,
            current_page=input_params.page,
            per_page=input_params.per_page,
            sort=input_params.sort,
            sort_dir=input_params.sort_dir,
            filter=input_params.filter,
        )