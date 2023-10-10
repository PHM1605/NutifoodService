from os import stat_result
from typing import Any, Optional
from pydantic import BaseModel


class CommonReponseBase(BaseModel):
    status: int = None
    code: str = None
    message: str = None
    data: Any = None


class CommonReponseCreate(CommonReponseBase):
    pass


class CommonReponse(CommonReponseBase):

    status: int = None
    code: str = None
    message: str = None
    data: Any = None

    def Ok(self, data_param: Any):
        self.data = data_param
        self.status = 200
        return self

    class Config:
        orm_mode = True
