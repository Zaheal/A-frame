from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from .template import templates
from src.config.project_config import get_settings

settings = get_settings()

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(
        request: Request,
        ):
    """
    
    :param request:
    :return:
    """
    return templates.TemplateResponse(request, "/login-page.html")


@router.get("/registration", response_class=HTMLResponse)
async def registration(
        request: Request,
        ):
    """
    
    :param request:
    :return:
    """

    return templates.TemplateResponse(request, "/registration-page.html")


@router.get("/reset-password")
async def reset_password(
        request: Request
        ):
    """
    
    :param request:
    :return:
    """
    return templates.TemplateResponse(request, "/reset_password-page.html")


@router.get("/edit-password/{token}", name="reset:edit_password")
async def edit_password(
        request: Request,
        token: str
        ):
    """
    
    :param request:
    :param token:
    :return:
    """
    
    return templates.TemplateResponse(request, "/edit_password-page.html", context={"token": token})
