from collections import namedtuple
from core.helpers.object_mapping_helper import ObjectMappingHelper
from core.internal.http_tenant import HttpTenant
from requests.models import Response
from core.schemas.base.tenant_conn_str_schema import TenantConnStrSchema
from core.helpers.database_connect_helper import DatabaseConnectHelper
from core.settings import get_settings

settings =  get_settings()


class ConnectionStringHelper():

    def getConnS(self) -> str:
        return settings.DATABASE_CONNECTION_STRING
