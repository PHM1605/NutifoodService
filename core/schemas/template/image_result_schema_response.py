
from pydantic.main import BaseModel


class ImageResultResponse(BaseModel):
    tenant_id: str 
    image_id: int
    image_code: str
    image_name: str
    image_date: str
    image_url: Optional[str]
    request_id: str
    program_code: str
    plan_code: str
    level_code: str
    criteria_code: str
    sku_group: str
    outlet_code: str
    route_code: str
    error: str
    image_result: int
    image_detail_results: str
    start_process: str
    end_process: str