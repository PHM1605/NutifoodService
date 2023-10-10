'''
    Logging, 
    Auth,
    Caching,
    Swagger Configuration,
    Request session handler
    etc.
'''
from fastapi.params import Depends, Header
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials, HTTPBearer
security = HTTPBearer()


async def get_tenant_header(Domain: str = Header(...), TenantId: str = Header(...)):
    return {'Domain': Domain, 'TenantId': TenantId}


async def has_access(Authorization: HTTPAuthorizationCredentials = Depends(security)):
    token = Authorization
    print("payload => ", token)
