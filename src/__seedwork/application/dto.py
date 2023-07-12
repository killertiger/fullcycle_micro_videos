from dataclasses import dataclass
from typing import Optional, TypeVar, Generic, List, Type
from __seedwork.domain.repositories import SearchResult

Filter = TypeVar('Filter')

@dataclass(slots=True, frozen=True)
class SearchInput(Generic[Filter]):
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None

Item = TypeVar('Item')

@dataclass(slots=True, frozen=True)
class PaginationOutput(Generic[Item]):
    items: List[Item]
    total: int
    current_page: int
    per_page: int
    last_page: int

Output = TypeVar('Output', bound=PaginationOutput)

@dataclass(slots=True, frozen=True)
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