
from sqlalchemy.sql.sqltypes import BOOLEAN, DATETIME, FLOAT, TEXT, INTEGER, TIME
from core.repositories.database_connection_repo import Base
from sqlalchemy import Column


class BaseModel(Base):
    IsDeleted = Column(BOOLEAN, nullable=False)
    CreatedBy = Column(TEXT)
    CreatedDate = Column(DATETIME, nullable=False)
    UpdatedBy = Column(TEXT)
    UpdatedDate = Column(DATETIME, nullable=False)
