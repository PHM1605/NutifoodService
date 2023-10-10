# function call Reposi

from typing import Optional
from core.schemas.base.database_helper_res_schema import DatabaseHelperReSchema
from requests.sessions import Session
from core.helpers.object_mapping_helper import ObjectMappingHelper
from sqlalchemy.engine.base import Engine
from core.repositories.database_connection_repo import DBRepository
from core.internal.http_tenant import HttpTenant


class DatabaseConnectHelper(DBRepository):

    def __init__(self, connStr: Optional[str]):
        DBRepository.__init__(self=self, connectionString=connStr)
