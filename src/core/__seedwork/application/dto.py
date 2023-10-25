from dataclasses import dataclass
from typing import Optional, TypeVar, Generic, List
from core.__seedwork.domain.repositories import SearchResult

Filter = TypeVar('Filter')


@dataclass(slots=True, frozen=True)
class SearchInput(Generic[Filter]):
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None
    
    def to_repository_input(self):
        return {
            'page': self.page,
            'per_page': self.per_page,
            'sort': self.sort,
            'sort_dir': self.sort_dir,
            'filter': self.filter
        }


PaginationOutputItem = TypeVar('PaginationOutputItem')


@dataclass(slots=True, frozen=True)
class PaginationOutput(Generic[PaginationOutputItem]):
    items: List[PaginationOutputItem]
    total: int
    current_page: int
    per_page: int
    last_page: int
    
    def from_search_result(cls, items: List[PaginationOutputItem], result: SearchResult):
        return cls(
            items=items,
            total=result.total,
            current_page=result.current_page,
            per_page=result.per_page,
            last_page=result.last_page
        )

# TODO: Remove PaginationOutputMapper
Output = TypeVar('Output', bound=PaginationOutput)
Item = TypeVar('Item', bound=PaginationOutput)

# TODO: Remove PaginationOutputMapper
# @dataclass(slots=True, frozen=True)
class PaginationOutputMapper:
    output_child: Output

    @staticmethod
    def from_child(output_child: Output):
        return PaginationOutputMapper(output_child)

    def to_output(self, items: List[Item], result: SearchResult) -> PaginationOutput[Item]:
        return self.output_child(
            items=items,
            total=result.total,
            current_page=result.current_page,
            per_page=result.per_page,
            last_page=result.last_page
        )
