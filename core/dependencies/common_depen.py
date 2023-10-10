from core.schemas.base.tenant_user_schema import TenantUserSchema
from middleware import get_tenant_header
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from core.internal.http_auth import HttpAuth
from typing import Union, Any
import jwt
from starlette.requests import Request
from datetime import datetime, timedelta
SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = f"spvb@dmspro.com"

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

async def get_info_user_tenant(request: Request, tenant=Depends(get_tenant_header)) -> str:
    domain = request.headers.get("Domain")
    tenantId = request.headers.get("TenantId")
    authorization = request.headers.get("Authorization")
    httpAuth = HttpAuth()
    user = await httpAuth.verifyTokenBrand(
        tenantId=tenantId, domain=domain, token=authorization)
    tenantUser = TenantUserSchema()
    tenantUser.domain = domain
    tenantUser.tenantId = tenantId
    tenantUser.userId = user.userId
    return tenantUser


def verify_password(username, password):
    if username == 'admin' and password == 'admin':
        return True
    return False

def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
    try:
        print("http_authorization_credentials.credentials: ", http_authorization_credentials.credentials)
        print("http_authorization_credentials.credentials: ", type(http_authorization_credentials.credentials))
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        experation_date = payload.get('exp')
        # experation_date = datetime.strptime(experation_date, '%M/%H/%m/%d/%Y')
        print(f'[x] Expiration date: {experation_date}')
        now = int(datetime.utcnow().strftime('%Y%m%d%H%M%S')) 
        if payload.get('exp') < now:
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('username')
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )

def generate_token(username: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * 300  # Expired after 3 days
    )
    expire = int(expire.strftime('%Y%m%d%H%M%S'))
    to_encode = {
        "exp": expire, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt