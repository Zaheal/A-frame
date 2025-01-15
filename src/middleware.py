from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        logger.debug(f"Request: {request.method} {request.url}")
        response: Response = await call_next(request)
        logger.debug(f"Response: {response.status_code}")
        return response
