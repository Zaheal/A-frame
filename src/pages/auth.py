from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from .template import templates


router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(
        request: Request
        ):
    """
    
    :param request:
    :return:
    """

    return templates.TemplateResponse(request, "login-page.html", context={"data": data})