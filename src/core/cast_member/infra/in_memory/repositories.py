from typing import List
from core.cast_member.domain.entities import CastMember
from core.cast_member.domain.repositories import CastMemberRepository
from core.__seedwork.domain.repositories import InMemorySearchableRepository, SortDirection

class CastMemberInMemoryRepository(CastMemberRepository, InMemorySearchableRepository):
    
    sortable_fields: List[str] = ['name', 'created_at']
    
    def _apply_filter(self, items: List[CastMember], filter_param: CastMemberRepository.SearchParams = None) -> List[CastMember]:
        if filter_param:
            filter_obj = filter(
                lambda item: self._filter_logic(item, filter_param),
                items
            )
            return list(filter_obj)
        
        return items
    
    def _filter_login(self, item: CastMember, filter_param: CastMemberRepository.SearchParams = None) -> bool:
        clause_name = lambda i: filter_param['name'].lower() in i.name.lower()
        clause_cast_member_type = lambda i: filter_param['cast_member_type'].value == i.cast_member_type.value
        
        if 'name' in filter_param and 'cast_member_type' in filter_param:
            return clause_name(item) and clause_cast_member_type(item)
        
        return clause_name(item) if 'name' in filter_param else clause_cast_member_type(item)
    
    def _apply_sort(self, items: List[CastMember], sort: SortDirection = None, sort_dir: str = None) -> List[CastMember]:
        return super()._apply_sort(items, sort, sort_dir) \
            if sort \
            else super()._apply_sort(items, 'created_at', SortDirection.Desc)