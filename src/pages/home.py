from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from .template import templates
from src.api.controllers.house_controllers import get_selected_house
from src.auth.user import current_active_user
from src.models.core_models import User, HouseModel
from src.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_class=HTMLResponse)
def homepage(
        request: Request,
        user: User | None = Depends(current_active_user),
        ):
    """
    Страница главной страницы

    :param request:
    :param user:
    :return:
    """

    return templates.TemplateResponse(request, "homepage.html", context={'user': user})


@router.get("/house/{house_id}", response_class=HTMLResponse)
async def house_page(
        request: Request,
        house: HouseModel = Depends(get_selected_house),
        user: User | None = Depends(current_active_user),
        ):
    """
    Страница для выбранного дома

    :param request:
    :param data:
    :param user:
    :return:
    """

    booked_dates = {}

    reservations = house.busy_times + house.temporary_busy_times

    for reserv in reservations:
        if reserv.end > datetime.now().date():
            start = str(reserv.start)
            if booked_dates.get(start[:4]):
                booked_dates[start[:4]].append([start[:10], str(reserv.end)[:10]])
            else: 
                booked_dates[start[:4]] = [[start[:10], str(reserv.end)[:10]]]
    
    return templates.TemplateResponse(request, "/house-page.html", context={"data": house, "booked_dates": booked_dates, "user": user})
