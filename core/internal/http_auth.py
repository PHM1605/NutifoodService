from core.schemas.base.tenant_user_schema import UserSchema
from core.settings import Settings
from core.schemas.base.tenant_conn_str_schema import TenantConnStrSchema
from requests.models import Response
from core.utils.constants import SERVICE_NAME
from core.internal.http_helper import HttpHelper


class HttpAuth(HttpHelper):

    async def verifyTokenBrand(self, tenantId: str, domain: str, token) -> UserSchema:
        settings = Settings()
        self.baseUrl = settings.AUTHOR_BRAND_URL
        self.authorization = token
        # TODO: Call api get connection string
        response: Response = self.get(
            apiPath="/{tenantId}/{domain}/api/v1/accounts/verify-token".format(tenantId=tenantId, domain=domain))
        data = response['data']
        user = UserSchema()
        user.userId = data['userId']
        return user
