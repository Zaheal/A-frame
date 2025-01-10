from datetime import date

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from .template import templates
from src.logger import get_logger
from src.config.project_config import get_settings
from src.auth.user import current_active_user, current_superuser, current_active_user_security
from src.api.controllers.user_reservation_controllers import get_user_reservations
from src.schemas.auth_schemas import UserRead

settings = get_settings()
logger = get_logger(__name__)

router = APIRouter()


def get_year_word(year):
    if 11 <= year % 100 <= 14:
        return "лет"
    elif year % 10 == 1:
        return "год"
    elif year % 10 in [2, 3, 4]:
        return "года"
    else:
        return "лет"
    

def get_month_word(month):
    if 11 <= month % 100 <= 14:
        return "месяцев"
    elif month % 10 == 1:
        return "месяц"
    elif month % 10 in [2, 3, 4]:
        return "месяца"
    else:
        return "месяцев"


@router.get("/profile", response_class=HTMLResponse, dependencies=[Depends(current_active_user_security)])
async def profile(
        request: Request,
        reservations = Depends(get_user_reservations),
        user = Depends(current_active_user)
        ):
    """
    
    :param request:
    :param reservations:
    :param user:
    :return:
    """

    
    delta = date.today() - user.created_at
    days = delta.days

    if days // 365 > 0:
        user.created_at = f'{days // 365} {get_year_word(days // 365)}'
    else:
        user.created_at = f'{days // 30} {get_month_word(days // 30)}'


    return templates.TemplateResponse(request, "/profile-page.html", context={"user_data": user, "reservations": reservations})


@router.get("/admin", response_class=HTMLResponse, dependencies=[Depends(current_superuser)])
async def admin(
        request: Request,
        user: UserRead = Depends(current_superuser)
        ):
    """
    
    :param request:
    :param user:
    :return:
    """

    return templates.TemplateResponse(request, "/admin-page.html", context={"user_data": user})
