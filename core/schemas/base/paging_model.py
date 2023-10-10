from typing import Any, List

from pydantic.main import BaseModel


class PagingSchema ():
    totalItems: int = 0
    pageIndex: int = 0
    pageSize: int = 0
    items: List[Any] = []


class PagingRequestSchema ():
    keyword:  str = ''
    sortBy:  str = None
    asc:  str = None
    pageSize: int = 0
    pageIndex: int = 0
