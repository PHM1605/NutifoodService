from typing import Any, Optional
from pydantic import BaseModel
from pydantic.main import BaseConfig
from sqlalchemy.orm import Session
from datetime import datetime



class DatabaseHelperResBase(BaseModel):
    engine: Any
    session: Any
    connector: Any


class DatabaseHelperResCreate(DatabaseHelperResBase):
    pass


class DatabaseHelperReSchema(DatabaseHelperResBase):
    engine: Any
    session: Any
    connector: Any

    class Config(BaseConfig):
        orm_mode: True
        arbitrary_types_allowed: False

