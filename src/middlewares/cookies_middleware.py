import uuid

from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_400_BAD_REQUEST

from src.logger import get_logger

logger = get_logger(__name__)


class CookiesMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,
                       request: Request,
                       call_next
                       ):
        response: Response = await call_next(request)
        user_id = request.cookies.get("user_id")
        try:
            if user_id is None:
                user_id = uuid.uuid4()
                response.set_cookie(key="user_id", value=user_id, httponly=True, path="/", samesite="lax")
            return response
        except Exception as e:
            logger.error("middleware dispatch failed", exc_info=e)
            return HTTPException(HTTP_400_BAD_REQUEST, e)
