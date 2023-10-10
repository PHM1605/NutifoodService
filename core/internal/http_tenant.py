from core.settings import Settings
from core.schemas.base.tenant_conn_str_schema import TenantConnStrSchema
from requests.models import Response
from core.utils.constants import SERVICE_NAME
from core.internal.http_helper import HttpHelper


class HttpTenant(HttpHelper):

    def getConnectionString(self, tenantId: str) -> Response:
        settings = Settings()
        self.baseUrl = settings.TENTAN_URL
        # TODO: Call api get connection string
        response: Response = self.get(
            apiPath="/api/v1/tenant-connections/get-connection/{tenantId}/{service}".format(tenantId=tenantId, service=SERVICE_NAME))

        return response
