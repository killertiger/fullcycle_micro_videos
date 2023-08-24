from abc import ABC
from typing import List, Any

from core.__seedwork.domain.repositories import (
    SearchableRepositoryInterface,
    SearchParams as DefaultSearchParams,
    SearchResult as DefaultSearchResult
)
from core.category.domain.entities import Category


class _SearchParams(DefaultSearchParams):  # pylint: disable=too-few-public-methods
    pass


class _SearchResult(DefaultSearchResult):  # pylint: disable=too-few-public-methods
    pass


class CategoryRepository(SearchableRepositoryInterface[Category, _SearchParams, _SearchResult],
                         ABC):
    SearchParams = _SearchParams
    SearchResult = _SearchResult
