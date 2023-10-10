from datetime import datetime
from pydantic import BaseModel


class TenantConnStrBase(BaseModel):
    def __init__(self, *, tenantId: str, tenantName: str, domain: str, service: str, connectionString: str) -> None:
        self.tenantId = tenantId
        self.tenantName = tenantName
        self.domain = domain
        self.service = service
        self.connectionString = connectionString


class TenantConnStrCreate(TenantConnStrBase):
    pass


class TenantConnStrSchema(TenantConnStrBase):
    tenantId: str = None
    tenantName: str = None
    domain: str = None
    service: str = None
    connectionString: str = None

    class Config:
        orm_mode = True


class BaseSchema(BaseModel):
    isDeleted: bool = False
    createdBy: str = None
    createdDate: datetime = None
    updatedBy: str = None
    updatedDate: datetime = None

    class Config:
        orm_mode = True
