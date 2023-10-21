from abc import ABC
from typing import Optional, TypedDict, Union
from core.__seedwork.domain.exceptions import SearchValidationException

from core.__seedwork.domain.repositories import (
    SearchableRepositoryInterface, SortDirection, SortDirectionValues, SearchParams as DefaultSearchParams, SearchResult as DefaultSearchResult)
from core.cast_member.domain.exceptions import InvalidCastMemberTypeException
from .entities import CastMember, CastMemberType


class _Filter(TypedDict):
    name: Optional[str]
    cast_member_type: Optional[CastMemberType]


class CreateFilterParam(TypedDict):
    name: Optional[str]
    cast_member_type: Optional[CastMemberType.TypeValues]


class _SearchParams(DefaultSearchParams[_Filter]):

    @staticmethod
    def create(
        page: int = DefaultSearchParams.get_field('page').default,
        per_page: int = DefaultSearchParams.get_field('per_page').default,
        filter: CreateFilterParam = None,
        sort: str = None,
        sort_dir: Union[None, SortDirectionValues, SortDirection] = None
    ) -> '_SearchParams':
        cast_member_type, error_cast_member_type = CastMemberType.create(filter['type']) \
            if isinstance(filter, dict) and 'type' in filter else (None, None)
            
        if error_cast_member_type:
            exception = SearchValidationException()
            exception.set_from_error('type', error_cast_member_type)
            raise exception

        return _SearchParams(
            page=page,
            per_page=per_page,
            filter=_Filter(
                name=filter['name'] if isinstance(
                    filter, dict) and 'name' in filter else None,
                cast_member_type=cast_member_type
            ),
            sort=sort,
            init_sort_dir=sort_dir,
        )

    def _normalize_filter(self):
        filter = self.filter if isinstance(self.filter, dict) else None
        
        if filter is None:
            return
        
        new_filter = _Filter()
        
        if 'name' in filter and filter['name']:
            new_filter['name'] = str(filter['name'])
            
        if 'cast_member_type' in filter and filter['cast_member_type']:
            if not isinstance(filter['cast_member_type'], CastMemberType):
                raise SearchValidationException({
                    'cast_member_type': [
                        str(InvalidCastMemberTypeException(filter['cast_member_type']))
                    ]
                })
            new_filter['cast_member_type'] = filter['cast_member_type']
            
        self.filter = new_filter or None
        
class _SearchResult(DefaultSearchResult):
    pass
    # def to_dict(self):
    #     data = super().to_dict()
    #     data['filter'] = {}
    #     if self.filter and self.filter['name']:
    #         data['filter']['name'] = self.filter['name']
    #     if self.filter and self.filter['cast_member_type']:
    #         data['filter']['cast_member_type'] = self.filter['cast_member_type'].value
    #     return data
    
class CastMemberRepository(
    SearchableRepositoryInterface[
        CastMember,
        _SearchParams,
        _SearchResult
    ],
    ABC
):
    SearchParams = _SearchParams
    SearchResult = _SearchResult
    Filter = _Filter