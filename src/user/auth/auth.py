
from authx import AuthX, AuthXConfig
from os import getenv

from dotenv import load_dotenv
from src.user.router import Request
from src.user.router import Response

load_dotenv()

config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY=getenv("JWT_SECRET_KEY"),
    JWT_ACCESS_COOKIE_NAME="access_token",
    JWT_REFRESH_COOKIE_NAME="refresh_token",
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_CSRF_PROTECT=True,
    JWT_CSRF_IN_COOKIES=True,
    JWT_CSRF_METHODS=["POST", "PUT", "PATCH", "DELETE"],
    JWT_ACCESS_CSRF_COOKIE_NAME="csrf_access_token",
    JWT_REFRESH_CSRF_COOKIE_NAME="csrf_refresh_token",
    JWT_ACCESS_CSRF_HEADER_NAME="X-CSRF-TOKEN",
    JWT_REFRESH_CSRF_HEADER_NAME="X-CSRF-REFRESH-TOKEN",
    JWT_COOKIE_SAMESITE="lax",
    JWT_COOKIE_DOMAIN="localhost",
    JWT_CSRF_CHECK_FORM=True,
)


authx = AuthX(config=config)

def create_jwt_token(username: str, response: Response) -> dict:
    token = authx.create_access_token(uid=username)
    refresh_token = authx.create_refresh_token(uid=username)
    authx.set_access_cookies(token, response)
    authx.set_refresh_cookies(refresh_token, response)
    return {"token": token, "refresh_token": refresh_token}

async def decode_jwt_token_in_get_request(request: Request) -> str:
    verify = await authx.get_access_token_from_request(request)
    payload = authx.verify_token(verify, verify_csrf=False)
    return payload.sub

async def decode_jwt_token_in_another_requests(request: Request) -> str:
    verify = await authx.get_access_token_from_request(request)
    payload = authx.verify_token(verify)
    return payload.sub

def logout_of_account(response: Response):
    try:
        authx.unset_cookies(response)
        return {"success": True, "message": "logout success"}
    except Exception as e:
        return {"success": False, "message": f"check this {e}"}