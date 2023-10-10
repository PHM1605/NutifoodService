from typing import Optional
from core.schemas.base.paging_model import PagingRequestSchema


async def common_param_paging(keyword: Optional[str] = None,
                              sortBy: Optional[str] = None, asc: Optional[bool] = None,
                              pageIndex: int = 0, pageSize: int = 10) -> PagingRequestSchema:
    result = PagingRequestSchema()
    result.keyword = keyword
    result.sortBy = sortBy
    result.asc = asc
    result.pageIndex = pageIndex
    result.pageSize = pageSize
    return result
