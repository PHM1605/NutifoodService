
from fastapi.params import Form
from typing import Union, Optional
from pydantic.main import BaseModel




"""{
tenant_id:    string($guid)
image_id:    integer($int32)
image_code:    string
image_name:    string
image_date:    datetime
image_path:    string
request_id:    string
program_code:    string
plan_code:    string
level_code:    string
criteria_code:    string
sku_group:    string
outet_code:    string
route_code:    string
error:    string
}"""
class ImageRequest(BaseModel):
    tenant_id: Optional[str] = None 
    image_id: Optional[int]
    image_code: Optional[str] = None
    image_name: Optional[str] = None
    image_date: Optional[str] = None
    image_url: Optional[str] = None
    request_id: Optional[str] = None
    program_code: Optional[str] = None
    plan_code: Optional[str] = None
    level_code: Optional[str] = None
    criteria_code: Optional[str] = None
    sku_group: Optional[str] = None
    outlet_code: Optional[str] = None
    route_code: Optional[str] = None
    error: Optional[str] = None
    time_get: Optional[str] = None
    time_sent: Optional[str] = None
    shots_id: Optional[int] = 0
    ship_to_code: Optional[str] = None
    posm_code: Optional[str] = None
    posm_type: Optional[str] = None
    tracking_code: Optional[str] = None
    number_of_floor: Optional[int] = 0
    iscombo: Optional[int] = 0

class LoginRequest(BaseModel):
    username: str
    password: str