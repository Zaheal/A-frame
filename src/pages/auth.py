import httpx

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .template import templates
from src.logger import get_logger
from src.config.project_config import get_settings

settings = get_settings()
logger = get_logger(__name__)

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


@router.post("/bridge/registration")
async def bridge_registration(
        name = Form(),
        email = Form(),
        password = Form(),
        number = Form()
        ):
    """
    
    :param name:
    :param email:
    :param password:
    :param number:
    :return:
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.SITE}/auth/register",
                                     json={"email": email, "password": password, "number": number, "name": name})
    logger.info(f"{response} regiser from bridge")

    return RedirectResponse("/login", status_code=303)


@router.get("/reset-password")
async def reset_password(
        request: Request
        ):

    return templates.TemplateResponse(request, "/reset_password-page.html")


@router.get("/edit-password/{token}")
async def edit_password(
        request: Request,
        token: str
        ):
    
    return templates.TemplateResponse(request, "/edit_password-page.html", context={"token": token})
